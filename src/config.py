import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
def get_logger(name: str):
    logger = logging.getLogger(name)
    # logger.addHandler(logging.StreamHandler(sys.stderr))
    logger.setLevel(logging.DEBUG)
    return logger

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
MESSAGES_LIMIT=50