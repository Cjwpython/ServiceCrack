import os

from colorlog import ColoredFormatter
import logging


def Logging(name, level="INFO"):
    if len(logging.root.handlers) > 0:  # see logging.basicConfig
        return logging.root
    LOGFORMAT = "[%(asctime)s][%(name)s][%(log_color)s**%(levelname)s**%(reset)s] [%(filename)s:%(funcName)s:%(log_color)s%(lineno)d%(reset)s] %(log_color)s%(message)s%(reset)s"
    logging.root.setLevel(getattr(logging, level))
    formatter = ColoredFormatter(LOGFORMAT)

    stream = logging.StreamHandler()
    stream.setLevel(getattr(logging, level))
    stream.setFormatter(formatter)

    log = logging.getLogger('logconfig')
    log.setLevel(logging.INFO)
    log.addHandler(stream)

    log = logging.getLogger(name)
    log.setLevel(getattr(logging, level))
    log.addHandler(stream)
    return log
