import logging
import logging.handlers
import sys

def get_logger(filename, level=logging.INFO, when='D', interval=1):
    """
    Get rotating logger, by default rotates every 1 day
    """
    # Setup logger
    logger = logging.getLogger('bot-log')
    logger.setLevel(level)

    # Setup handlers
    file_handler = logging.handlers.TimedRotatingFileHandler(filename, when, interval, utc=True)
    console_handler = logging.StreamHandler(sys.stdout)

    # Set format
    formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
