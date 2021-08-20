import os

from colorlog import ColoredFormatter
import logging

LOGFORMAT = "[%(asctime)s][%(name)s] [%(log_color)s**%(levelname)s**%(reset)s] [%(filename)s:%(funcName)s:%(log_color)s%(lineno)d%(reset)s] %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(logging.INFO)
formatter = ColoredFormatter(LOGFORMAT)

stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
stream.setFormatter(formatter)

log = logging.getLogger('logconfig')
log.setLevel(logging.INFO)
log.addHandler(stream)


def Logging(name):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    log.addHandler(stream)
    return log
