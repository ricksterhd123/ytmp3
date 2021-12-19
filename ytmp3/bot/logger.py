import logging
import logging.handlers

def get_logger(filename, level=logging.INFO, when='D', interval=1):
    """
    Get rotating logger, by default rotates every 1 day
    """
    logger = logging.getLogger('bot-log')
    logger.setLevel(level)
    handler = logging.handlers.TimedRotatingFileHandler(filename, when, interval, utc=True)
    formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
