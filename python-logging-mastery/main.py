"""
ETL Pipeline -- Main Orchestrator
===================================

This is the entry point. It ties together:
    1. Logging configuration (run once, used everywhere)
    2. Extract phase  (read from CSV, JSON, API)
    3. Transform phase (clean, validate, enrich)
    4. Load phase     (write to SQLite database)

Run this file:
    python main.py

After running, inspect:
    - Console output          -- shows INFO+ logs (operator view)
    - logs/pipeline.log       -- shows DEBUG+ logs (full forensic detail)
    - logs/errors.log         -- shows ERROR+ logs (on-call triage view)
    - output/clean_sales.db   -- the loaded SQLite database

KEY LOGGING CONCEPT:
    logging.exception() is used in the except blocks below. It automatically
    captures the full stack trace at ERROR level, which is invaluable for
    debugging production failures.
"""

import logging
import os
import sys
import time

# Add the project root to the path so imports work when running directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.logging_config import setup_logging
from etl.extractor import run_extraction
from etl.transformer import run_transformation
from etl.loader import run_loading

# Get a logger for this module
logger = logging.getLogger(__name__)


def run_pipeline():
    """
    Execute the full ETL pipeline with comprehensive logging at every stage.
    """
    # ------------------------------------------------------------------
    # STEP 1: Initialize logging FIRST, before anything else
    # ------------------------------------------------------------------
    setup_logging(log_dir="logs")

    logger.info("=" * 60)
    logger.info("ETL PIPELINE STARTED")
    logger.info("=" * 60)
    logger.info("Working directory: %s", os.getcwd())

    start_time = time.time()

    # Track pipeline stats
    stats = {
        "extracted": 0,
        "transformed": 0,
        "loaded": 0,
        "skipped": 0,
        "errors": 0,
        "phase_failed": None,
    }

    # ------------------------------------------------------------------
    # STEP 2: EXTRACT -- Read raw data from sources
    # ------------------------------------------------------------------
    try:
        extracted_data = run_extraction(
            csv_path="data/sales_data.csv",
            json_path="data/products.json"
        )
        stats["extracted"] = len(extracted_data["sales_data"])
    except Exception:
        # logging.exception() captures the full traceback automatically
        logger.exception("EXTRACTION PHASE FAILED -- see traceback below")
        stats["phase_failed"] = "extraction"
        stats["errors"] += 1
        logger.critical("Pipeline aborted during extraction. Check logs/errors.log for details.")
        return stats

    # ------------------------------------------------------------------
    # STEP 3: TRANSFORM -- Clean, validate, enrich
    # ------------------------------------------------------------------
    try:
        cleaned_rows = run_transformation(extracted_data)
        stats["transformed"] = len(cleaned_rows)
    except Exception:
        logger.exception("TRANSFORMATION PHASE FAILED -- see traceback below")
        stats["phase_failed"] = "transformation"
        stats["errors"] += 1
        logger.critical("Pipeline aborted during transformation. Check logs/errors.log for details.")
        return stats

    # ------------------------------------------------------------------
    # STEP 4: LOAD -- Write to database
    # ------------------------------------------------------------------
    try:
        inserted, skipped = run_loading(cleaned_rows, db_path="output/clean_sales.db")
        stats["loaded"] = inserted
        stats["skipped"] = skipped
    except Exception:
        logger.exception("LOADING PHASE FAILED -- see traceback below")
        stats["phase_failed"] = "loading"
        stats["errors"] += 1
        logger.critical("Pipeline aborted during loading. Check logs/errors.log for details.")
        return stats

    # ------------------------------------------------------------------
    # STEP 5: Pipeline Summary
    # ------------------------------------------------------------------
    elapsed = round(time.time() - start_time, 2)

    logger.info("=" * 60)
    logger.info("ETL PIPELINE COMPLETED SUCCESSFULLY")
    logger.info("=" * 60)
    logger.info("Elapsed time:     %s seconds", elapsed)
    logger.info("Rows extracted:   %d", stats["extracted"])
    logger.info("Rows transformed: %d", stats["transformed"])
    logger.info("Rows loaded:      %d", stats["loaded"])
    logger.info("Rows skipped:     %d", stats["skipped"])
    logger.info("=" * 60)
    logger.info("Log files written to: logs/")
    logger.info("  - logs/pipeline.log  (full DEBUG detail)")
    logger.info("  - logs/errors.log    (ERROR+ only)")
    logger.info("Database written to:   output/clean_sales.db")
    logger.info("=" * 60)

    return stats


if __name__ == "__main__":
    run_pipeline()
