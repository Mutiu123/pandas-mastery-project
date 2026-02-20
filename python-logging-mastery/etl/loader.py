"""
LOAD Phase -- Write cleaned data to SQLite database
=====================================================

This module takes the cleaned, validated, enriched data and loads it into
a SQLite database in batches. It handles database creation, batch inserts,
integrity errors, and simulates connection failures.

LOG LEVELS USED:
    DEBUG    -- SQL statements, batch progress, commit details
    INFO     -- table creation, batch completion, final row counts
    WARNING  -- duplicate records skipped (ON CONFLICT IGNORE)
    ERROR    -- batch insert failures, integrity constraint violations
    CRITICAL -- database connection lost mid-load, data rollback
"""

import logging
import os
import random
import sqlite3

logger = logging.getLogger(__name__)

BATCH_SIZE = 10  # Small batch size for demo -- real pipelines use 1000+


def create_database(db_path):
    """
    Create the SQLite database and the target table.

    Demonstrates:
        - DEBUG for SQL DDL statements
        - INFO for successful creation
        - ERROR if database creation fails
    """
    logger.debug("Creating database at: %s", os.path.abspath(db_path))

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        create_sql = """
        CREATE TABLE IF NOT EXISTS clean_sales (
            order_id       TEXT PRIMARY KEY,
            customer_name  TEXT,
            email          TEXT,
            product_id     TEXT,
            product_name   TEXT,
            category       TEXT,
            quantity        INTEGER,
            unit_price     REAL,
            total          REAL,
            order_date     TEXT,
            payment_method TEXT,
            current_stock  INTEGER,
            anomaly_flags  TEXT
        )
        """
        logger.debug("Executing DDL:\n%s", create_sql.strip())
        cursor.execute(create_sql)
        conn.commit()

        logger.info("Database table 'clean_sales' created (or already exists) at '%s'", db_path)
        return conn

    except sqlite3.Error as e:
        logger.error("Failed to create database at '%s': %s", db_path, e)
        raise


def load_batch(cursor, batch, batch_num):
    """
    Insert a batch of rows into the database.

    Demonstrates:
        - DEBUG for per-batch SQL details
        - WARNING for duplicate handling
        - ERROR for constraint violations
    """
    insert_sql = """
    INSERT OR IGNORE INTO clean_sales
        (order_id, customer_name, email, product_id, product_name, category,
         quantity, unit_price, total, order_date, payment_method, current_stock,
         anomaly_flags)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    logger.debug("Batch %d: Inserting %d rows", batch_num, len(batch))

    inserted = 0
    skipped = 0

    for row in batch:
        try:
            cursor.execute(insert_sql, (
                row["order_id"],
                row["customer_name"],
                row["email"],
                row["product_id"],
                row.get("product_name", "UNKNOWN"),
                row.get("category", "UNKNOWN"),
                row["quantity"],
                row["unit_price"],
                row["total"],
                row["order_date"],
                row["payment_method"],
                row.get("current_stock", -1),
                str(row.get("anomaly_flags", [])),
            ))
            if cursor.rowcount > 0:
                inserted += 1
            else:
                skipped += 1
                logger.warning(
                    "Batch %d: Duplicate order '%s' skipped (INSERT OR IGNORE)",
                    batch_num, row["order_id"]
                )
        except sqlite3.IntegrityError as e:
            skipped += 1
            logger.error(
                "Batch %d: IntegrityError on order '%s': %s",
                batch_num, row["order_id"], e
            )

    logger.debug("Batch %d result: %d inserted, %d skipped", batch_num, inserted, skipped)
    return inserted, skipped


def simulate_connection_issue(batch_num, total_batches):
    """
    Randomly simulate a database connection failure to demonstrate
    CRITICAL-level logging and rollback handling.

    In real ETL pipelines, this happens due to:
        - Network timeouts to remote databases
        - Database server restarts during maintenance windows
        - Disk full on the database server
    """
    # Only trigger on the last batch with a 30% chance (for demo purposes)
    if batch_num == total_batches and random.random() < 0.3:
        return True
    return False


def run_loading(cleaned_rows, db_path="output/clean_sales.db"):
    """
    Run the full loading phase.

    Inserts rows in batches and handles errors gracefully.
    """
    logger.info("=" * 60)
    logger.info("LOADING PHASE STARTED")
    logger.info("=" * 60)

    logger.info("Target database: %s", os.path.abspath(db_path))
    logger.info("Batch size: %d rows", BATCH_SIZE)
    logger.info("Total rows to load: %d", len(cleaned_rows))

    # Create database and table
    conn = create_database(db_path)
    cursor = conn.cursor()

    # Split rows into batches
    batches = [
        cleaned_rows[i:i + BATCH_SIZE]
        for i in range(0, len(cleaned_rows), BATCH_SIZE)
    ]
    total_batches = len(batches)
    logger.info("Split into %d batches", total_batches)

    total_inserted = 0
    total_skipped = 0

    for batch_num, batch in enumerate(batches, start=1):
        logger.debug("Processing batch %d/%d...", batch_num, total_batches)

        # Simulate potential connection failure
        if simulate_connection_issue(batch_num, total_batches):
            logger.critical(
                "Database connection lost during batch %d/%d! "
                "%d rows in this batch were NOT committed. Attempting rollback...",
                batch_num, total_batches, len(batch)
            )
            try:
                conn.rollback()
                logger.error(
                    "Rollback successful. %d rows from batch %d were lost. "
                    "Previously committed batches (%d rows) are safe.",
                    len(batch), batch_num, total_inserted
                )
            except sqlite3.Error as e:
                logger.critical("Rollback FAILED: %s -- database may be in inconsistent state", e)
            break

        # Normal batch processing
        inserted, skipped = load_batch(cursor, batch, batch_num)
        total_inserted += inserted
        total_skipped += skipped

        # Commit after each batch (not after each row -- more efficient)
        conn.commit()
        logger.debug("Batch %d committed to database", batch_num)

    # Final summary
    conn.close()
    logger.info(
        "LOADING COMPLETE -- %d rows inserted, %d duplicates skipped",
        total_inserted, total_skipped
    )

    if total_skipped > 0:
        logger.warning(
            "%d records were skipped during loading (duplicates or constraint violations)",
            total_skipped
        )

    return total_inserted, total_skipped
