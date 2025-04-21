import logging
import logging.config
import os
from typing import Optional



def setup_logger(name: str, log_file: str = "logs/app.log") -> logging.Logger:
    """Set up and return a configured logger for the given module name.
    
    Args:
        name(str): Name of the logger.
        log_file(str): Path to log file(Default "app.log")

    Returns: 
        logging.Logger: Configured logger instance
    """

    # Ensure directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers if logger is already configured
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console handler (INFO and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # File handler (DEBUG and above)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger



if __name__ == "__main__":
    # Example usage     
    logger = setup_logger(__name__, "logs/app.log")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")

