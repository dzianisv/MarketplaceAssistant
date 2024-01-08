import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
def get_logger(name: str):
    logger = logging.getLogger(name)
    # logger.addHandler(logging.StreamHandler(sys.stderr))
    logger.setLevel(logging.DEBUG)
    return logger

with open("message.txt", "r", encoding='utf8') as m:
    MESSAGE = m.read()

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
