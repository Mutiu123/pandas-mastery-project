"""
TRANSFORM Phase -- Clean, validate, and enrich raw data
=========================================================

This module takes the raw extracted data and:
    1. Validates each row (types, required fields, value ranges)
    2. Cleans dirty data (fills missing values, fixes negatives)
    3. Enriches rows with product catalog info
    4. Flags anomalies (unusually large orders, suspicious patterns)

LOG LEVELS USED:
    DEBUG    -- per-row transformation details
    INFO     -- phase summaries, row counts in/out
    WARNING  -- data quality issues that were auto-corrected
    ERROR    -- rows that had to be skipped entirely
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Thresholds for anomaly detection
HIGH_VALUE_ORDER_THRESHOLD = 500.00
HIGH_QUANTITY_THRESHOLD = 20
LOW_STOCK_THRESHOLD = 10


def validate_row(row, row_num):
    """
    Validate a single row of sales data. Returns (is_valid, cleaned_row, issues).

    Demonstrates how logging helps trace EXACTLY which rows have problems
    and what was done about each one.
    """
    issues = []
    cleaned = dict(row)

    # --- Validate required fields ---
    if not row.get("order_id"):
        logger.error("Row %d: Missing required field 'order_id' -- skipping row", row_num)
        return False, None, ["missing_order_id"]

    if not row.get("product_id"):
        logger.error("Row %d (order %s): Missing required field 'product_id' -- skipping row", row_num, row["order_id"])
        return False, None, ["missing_product_id"]

    # --- Validate and clean email ---
    if not row.get("email"):
        logger.warning("Row %d (order %s): Missing 'email' field -- filling with 'unknown@placeholder.com'", row_num, row["order_id"])
        cleaned["email"] = "unknown@placeholder.com"
        issues.append("missing_email")

    # --- Validate quantity ---
    try:
        quantity = int(row["quantity"])
        if quantity <= 0:
            logger.warning(
                "Row %d (order %s): Negative or zero quantity (%s) -- setting to 1",
                row_num, row["order_id"], row["quantity"]
            )
            quantity = 1
            issues.append("invalid_quantity")
        cleaned["quantity"] = quantity
    except (ValueError, TypeError):
        logger.error(
            "Row %d (order %s): Quantity '%s' is not a valid integer -- skipping row",
            row_num, row["order_id"], row.get("quantity")
        )
        return False, None, ["invalid_quantity_type"]

    # --- Validate unit_price ---
    try:
        price = float(row["unit_price"]) if row.get("unit_price") else 0.0
        if price < 0:
            logger.warning(
                "Row %d (order %s): Negative price ($%.2f) -- setting to $0.00",
                row_num, row["order_id"], price
            )
            price = 0.0
            issues.append("negative_price")
        elif price == 0.0:
            logger.warning(
                "Row %d (order %s): Price is $0.00 -- possible data entry error",
                row_num, row["order_id"]
            )
            issues.append("zero_price")
        cleaned["unit_price"] = price
    except (ValueError, TypeError):
        logger.error(
            "Row %d (order %s): Price '%s' is not a valid number -- skipping row",
            row_num, row["order_id"], row.get("unit_price")
        )
        return False, None, ["invalid_price_type"]

    # --- Validate order_date ---
    date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%b %d %Y"]
    parsed_date = None
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(row["order_date"], fmt)
            break
        except (ValueError, TypeError):
            continue

    if parsed_date is None:
        logger.error(
            "Row %d (order %s): Date '%s' does not match any known format -- skipping row",
            row_num, row["order_id"], row.get("order_date")
        )
        return False, None, ["unparseable_date"]

    cleaned["order_date"] = parsed_date.strftime("%Y-%m-%d")
    logger.debug("Row %d: Parsed date '%s' -> '%s'", row_num, row["order_date"], cleaned["order_date"])

    # --- Calculate total ---
    cleaned["total"] = round(cleaned["quantity"] * cleaned["unit_price"], 2)

    return True, cleaned, issues


def detect_anomalies(row, row_num):
    """
    Flag suspicious patterns that might need human review.

    Demonstrates WARNING-level logging for business logic alerts.
    """
    alerts = []

    total = row.get("total", 0)
    if total > HIGH_VALUE_ORDER_THRESHOLD:
        logger.warning(
            "Row %d (order %s): High-value order detected ($%.2f) -- flagged for review",
            row_num, row["order_id"], total
        )
        alerts.append("high_value")

    quantity = row.get("quantity", 0)
    if quantity > HIGH_QUANTITY_THRESHOLD:
        logger.warning(
            "Row %d (order %s): Unusually high quantity (%d units) -- possible bulk/fraud",
            row_num, row["order_id"], quantity
        )
        alerts.append("high_quantity")

    return alerts


def enrich_with_products(rows, product_catalog):
    """
    Add product name and category from the product catalog.

    Demonstrates DEBUG logging for enrichment details and WARNING
    for missing product references.
    """
    logger.info("Enriching %d rows with product catalog (%d products)", len(rows), len(product_catalog))

    # Build a lookup dict
    product_lookup = {p["product_id"]: p for p in product_catalog}
    enriched = []
    missing_products = set()

    for row in rows:
        product = product_lookup.get(row["product_id"])
        if product:
            row["product_name"] = product["name"]
            row["category"] = product["category"]
            row["current_stock"] = product["stock"]
            logger.debug(
                "Enriched order %s with product '%s' (stock: %d)",
                row["order_id"], product["name"], product["stock"]
            )

            # Check stock levels
            if product["stock"] < LOW_STOCK_THRESHOLD:
                logger.warning(
                    "Low stock alert: '%s' (ID: %s) has only %d units remaining",
                    product["name"], product["product_id"], product["stock"]
                )
        else:
            missing_products.add(row["product_id"])
            row["product_name"] = "UNKNOWN"
            row["category"] = "UNKNOWN"
            row["current_stock"] = -1

        enriched.append(row)

    if missing_products:
        logger.warning(
            "%d product IDs in sales data not found in catalog: %s",
            len(missing_products), sorted(missing_products)
        )

    return enriched


def check_duplicates(rows):
    """
    Detect and remove duplicate order IDs.

    Demonstrates INFO/WARNING logging for data deduplication.
    """
    seen = {}
    unique_rows = []
    duplicate_count = 0

    for row in rows:
        order_id = row["order_id"]
        if order_id in seen:
            duplicate_count += 1
            logger.warning(
                "Duplicate order_id '%s' detected (first seen at position %d) -- removing duplicate",
                order_id, seen[order_id]
            )
        else:
            seen[order_id] = len(unique_rows)
            unique_rows.append(row)

    if duplicate_count > 0:
        logger.info("Removed %d duplicate records", duplicate_count)
    else:
        logger.debug("No duplicates found")

    return unique_rows


def run_transformation(extracted_data):
    """
    Run the full transformation phase.

    Takes raw extracted data, returns cleaned and enriched rows.
    """
    logger.info("=" * 60)
    logger.info("TRANSFORMATION PHASE STARTED")
    logger.info("=" * 60)

    raw_rows = extracted_data["sales_data"]
    product_catalog = extracted_data["product_catalog"]

    logger.info("Input: %d raw sales rows, %d products in catalog", len(raw_rows), len(product_catalog))

    # Step 1: Validate and clean each row
    valid_rows = []
    skipped_rows = 0
    total_issues = {}

    for i, row in enumerate(raw_rows, start=1):
        logger.debug("Processing row %d/%d: order_id=%s", i, len(raw_rows), row.get("order_id", "N/A"))
        is_valid, cleaned, issues = validate_row(row, i)

        if is_valid:
            valid_rows.append(cleaned)
            # Track issue counts for summary
            for issue in issues:
                total_issues[issue] = total_issues.get(issue, 0) + 1
        else:
            skipped_rows += 1

    logger.info(
        "Validation complete: %d valid rows, %d skipped",
        len(valid_rows), skipped_rows
    )
    if total_issues:
        logger.info("Auto-corrected issues: %s", total_issues)

    # Step 2: Remove duplicates
    valid_rows = check_duplicates(valid_rows)

    # Step 3: Detect anomalies
    logger.info("Running anomaly detection...")
    anomaly_count = 0
    for i, row in enumerate(valid_rows, start=1):
        alerts = detect_anomalies(row, i)
        if alerts:
            row["anomaly_flags"] = alerts
            anomaly_count += 1
        else:
            row["anomaly_flags"] = []

    logger.info("Anomaly detection complete: %d rows flagged", anomaly_count)

    # Step 4: Enrich with product data
    valid_rows = enrich_with_products(valid_rows, product_catalog)

    logger.info(
        "TRANSFORMATION COMPLETE -- %d rows in -> %d clean rows out "
        "(%d skipped, %d anomalies flagged)",
        len(raw_rows), len(valid_rows), skipped_rows, anomaly_count
    )

    return valid_rows
