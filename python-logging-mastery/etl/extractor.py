"""
EXTRACT Phase -- Read raw data from sources
=============================================

This module reads data from CSV files, JSON files, and simulates pulling from
a flaky REST API. It demonstrates logging at every severity level in a context
that makes real-world sense.

LOG LEVELS USED:
    DEBUG    -- file paths resolved, byte counts, raw row counts
    INFO     -- successful extractions with summary counts
    WARNING  -- stale files, missing optional sources
    ERROR    -- API failures with retries
    CRITICAL -- all sources failed, pipeline cannot continue
"""

import csv
import json
import logging
import os
import random
import time
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Named logger: appears as "etl.extractor" in logs because __name__ resolves
# to "etl.extractor" when this module is imported from the etl package.
# This lets you filter logs per module.
# ---------------------------------------------------------------------------
logger = logging.getLogger(__name__)


def extract_csv(file_path):
    """
    Extract rows from a CSV file.

    Demonstrates:
        - DEBUG for low-level details (file size, row count)
        - INFO for successful completion
        - WARNING if file is older than 7 days
        - ERROR if file is missing or unreadable
    """
    logger.debug("Attempting to extract CSV from: %s", os.path.abspath(file_path))

    if not os.path.exists(file_path):
        logger.error("CSV file not found: %s", file_path)
        return []

    # Check file age -- in production, stale data can cause subtle bugs
    file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    file_age = datetime.now() - file_mod_time
    if file_age > timedelta(days=7):
        logger.warning(
            "CSV file '%s' is %d days old -- data may be stale",
            os.path.basename(file_path),
            file_age.days
        )

    # Read the file
    file_size = os.path.getsize(file_path)
    logger.debug("File size: %d bytes", file_size)

    rows = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))

    logger.info("Successfully extracted %d rows from '%s'", len(rows), os.path.basename(file_path))
    logger.debug("Column names: %s", list(rows[0].keys()) if rows else "N/A")

    return rows


def extract_json(file_path, key="products"):
    """
    Extract records from a JSON file under a specific key.

    Demonstrates:
        - DEBUG for parsing details
        - INFO for success
        - ERROR for malformed JSON
    """
    logger.debug("Attempting to extract JSON from: %s (key='%s')", os.path.abspath(file_path), key)

    if not os.path.exists(file_path):
        logger.error("JSON file not found: %s", file_path)
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse JSON file '%s': %s", file_path, e)
        return []

    if key not in data:
        logger.error("Expected key '%s' not found in JSON. Available keys: %s", key, list(data.keys()))
        return []

    records = data[key]
    logger.info("Successfully extracted %d records from '%s' (key='%s')", len(records), os.path.basename(file_path), key)
    logger.debug("First record sample: %s", records[0] if records else "N/A")

    return records


def extract_from_api(url="https://api.example.com/sales", max_retries=3):
    """
    Simulate extracting data from a flaky REST API with retries.

    This is a SIMULATION -- no real HTTP calls are made. But the logging
    patterns here are exactly what you'd use in production with requests/httpx.

    Demonstrates:
        - INFO for attempt starts
        - WARNING for retries
        - ERROR for individual failures
        - CRITICAL when all retries are exhausted
    """
    logger.info("Starting API extraction from: %s", url)

    for attempt in range(1, max_retries + 1):
        logger.debug("API request attempt %d/%d", attempt, max_retries)

        # Simulate a flaky API -- fails randomly
        # In real code this would be: response = requests.get(url, timeout=30)
        simulated_status = random.choice([200, 200, 503, 500, 200])

        if simulated_status == 200:
            logger.info("API returned 200 OK on attempt %d", attempt)
            # Return simulated data
            return [
                {"source": "api", "order_id": "API-001", "amount": 150.00},
                {"source": "api", "order_id": "API-002", "amount": 75.50},
            ]

        # Non-200 response -- log as error and maybe retry
        logger.error(
            "API request failed -- HTTP %d from %s (attempt %d/%d)",
            simulated_status, url, attempt, max_retries
        )

        if attempt < max_retries:
            wait_time = 2 ** attempt  # Exponential backoff: 2s, 4s, 8s
            logger.warning("Retrying in %d seconds (exponential backoff)...", wait_time)
            time.sleep(0.1)  # Shortened for demo; real code would use wait_time
        else:
            logger.critical(
                "All %d API extraction attempts failed for %s. "
                "Pipeline will continue without API data.",
                max_retries, url
            )

    return []


def run_extraction(csv_path, json_path):
    """
    Run the full extraction phase: CSV + JSON + API.

    Returns a dict with all extracted data.
    """
    logger.info("=" * 60)
    logger.info("EXTRACTION PHASE STARTED")
    logger.info("=" * 60)

    results = {
        "sales_data": [],
        "product_catalog": [],
        "api_data": [],
    }

    # Extract CSV (primary source)
    results["sales_data"] = extract_csv(csv_path)

    # Extract JSON (product catalog for enrichment)
    results["product_catalog"] = extract_json(json_path)

    # Extract from API (supplementary data)
    results["api_data"] = extract_from_api()

    total_records = sum(len(v) for v in results.values())
    logger.info(
        "EXTRACTION COMPLETE -- Total records extracted: %d "
        "(CSV: %d, JSON: %d, API: %d)",
        total_records,
        len(results["sales_data"]),
        len(results["product_catalog"]),
        len(results["api_data"])
    )

    if not results["sales_data"]:
        logger.critical("Primary data source (CSV) returned zero records. Pipeline cannot continue.")
        raise RuntimeError("Extraction failed: no sales data")

    return results
