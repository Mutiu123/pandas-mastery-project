"""
Centralized Logging Configuration for the ETL Pipeline
=======================================================

This module sets up the entire logging system for the pipeline. Instead of
calling basicConfig() everywhere, we configure logging ONCE here and every
module gets its own named logger via logging.getLogger(__name__).

KEY CONCEPTS DEMONSTRATED:
    1. Named loggers       -- each module gets its own logger (etl.extractor, etc.)
    2. Multiple handlers   -- console, full log file, error-only log file
    3. Different levels    -- console shows INFO+, file captures DEBUG+, error file captures ERROR+
    4. Custom formatters   -- timestamps, module names, line numbers
    5. RotatingFileHandler -- prevents log files from growing forever
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(log_dir="logs"):
    """
    Configure the root logger with three handlers:
        - Console:    Shows INFO and above (what operators see in real time)
        - File:       Captures DEBUG and above (full detail for forensic analysis)
        - Error file: Captures ERROR and above (quick triage for on-call engineers)

    Args:
        log_dir: Directory where log files will be written. Created if it doesn't exist.
    """

    # Create the logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # -------------------------------------------------------------------------
    # STEP 1: Get the ROOT logger
    # -------------------------------------------------------------------------
    # The root logger is the parent of all loggers. By configuring it here,
    # every logger created with logging.getLogger(__name__) in other modules
    # will inherit these handlers.
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture everything; handlers will filter

    # Clear any existing handlers (important if running in notebooks or re-importing)
    root_logger.handlers.clear()

    # -------------------------------------------------------------------------
    # STEP 2: Define formatters
    # -------------------------------------------------------------------------
    # Detailed formatter for files -- includes timestamp, level, logger name,
    # source file, line number, and the message
    file_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-20s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Shorter formatter for console -- operators don't need file/line info in real time
    console_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    )

    # -------------------------------------------------------------------------
    # STEP 3: Console Handler (INFO+)
    # -------------------------------------------------------------------------
    # This is what the operator sees when they run the pipeline.
    # We set it to INFO so they see progress updates, warnings, and errors,
    # but NOT the verbose DEBUG noise.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # -------------------------------------------------------------------------
    # STEP 4: File Handler with rotation (DEBUG+)
    # -------------------------------------------------------------------------
    # This captures EVERYTHING for post-mortem analysis.
    # RotatingFileHandler rolls over when the file hits maxBytes and keeps
    # backupCount old files (pipeline.log, pipeline.log.1, pipeline.log.2, etc.)
    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "pipeline.log"),
        maxBytes=5 * 1024 * 1024,  # 5 MB per file
        backupCount=3,             # Keep 3 old files
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # -------------------------------------------------------------------------
    # STEP 5: Error-only file handler (ERROR+)
    # -------------------------------------------------------------------------
    # On-call engineers check this file first to see what went wrong,
    # without wading through thousands of DEBUG/INFO lines.
    error_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "errors.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)

    # -------------------------------------------------------------------------
    # STEP 6: Attach all handlers to the root logger
    # -------------------------------------------------------------------------
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)

    # Log that the system is ready (this itself gets captured)
    logging.info("Logging system initialized -- console=INFO, file=DEBUG, errors=ERROR")
    logging.debug("Log directory: %s", os.path.abspath(log_dir))
