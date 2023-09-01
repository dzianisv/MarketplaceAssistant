import os
import logging


logging.basicConfig(level=logging.DEBUG)
def get_logger(name: str):
    return logging.getLogger(name)

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
