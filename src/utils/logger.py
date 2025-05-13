import logging
import logging.handlers
import os
from typing import Optional
from pathlib import Path
from datetime import datetime

def setup_logger(name: str, log_file: str = "logs/app.log") -> logging.Logger:
    """Set up and return a configured logger for the given module name.

    Args:
        name: Name of the logger.
        log_file: Path to log file (Default: 'logs/app.log').

    Returns:
        logging.Logger: Configured logger instance with daily rotation and size limit.
    """
    # Ensure directory exists
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console handler (INFO and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Timed rotating file handler for daily rotation
        base, ext = os.path.splitext(log_file)
        dated_log_file = f"{base}-{datetime.now().strftime('%Y-%m-%d')}{ext}"
        file_handler = logging.handlers.TimedRotatingFileHandler(
            dated_log_file,
            when="midnight",  # Rotate at midnight
            interval=1,       # Every 1 day
            backupCount=30,   # Keep 30 days of logs
            encoding="utf-8"  # Support emojis
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Custom size check for 1 MB limit
        def check_size_and_rotate():
            try:
                if os.path.exists(file_handler.baseFilename) and os.path.getsize(file_handler.baseFilename) > 1_000_000:
                    file_handler.doRollover()
                    # Update baseFilename to new rotated file
                    file_handler.baseFilename = f"{base}-{datetime.now().strftime('%Y-%m-%d')}{ext}"
            except Exception as e:
                logger.error(f"Error during size-based rotation: {e}")

        file_handler.check_size = check_size_and_rotate

        # Custom namer to avoid premature size checks
        def namer(name):
            base, ext = os.path.splitext(name)
            return f"{base}.{datetime.now().strftime('%H-%M-%S')}{ext}"
        file_handler.namer = namer

        # Add handlers to logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        # Ensure logger doesn't propagate to parent loggers
        logger.propagate = False

    return logger



