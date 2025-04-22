from src.utils.logger import setup_logger
import time

logger = setup_logger(__name__, "logs/test.log")
logger.debug("Starting test")
# Simulate large log writes
for i in range(10000):
    logger.debug(f"Test message {i}: {'x' * 100}")
    # Check size and rotate
    for handler in logger.handlers:
        if hasattr(handler, "check_size"):
            handler.check_size()
logger.info("Test complete 🔍")