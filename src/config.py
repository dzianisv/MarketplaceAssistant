import os
import logging


logging.basicConfig(level=logging.DEBUG)
def get_logger(name: str):
    return logging.getLogger(name)


with open("message.txt", "r", encoding='utf8') as m:
    MESSAGE = m.read()

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
