import logging
from logging.handlers import RotatingFileHandler

def init_worker_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s - %(name)s :: %(line)s - %(levelname)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = RotatingFileHandler(filename="/tmp/worker.log", maxBytes=2, backupCount=2) 
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(fh)

def init_block_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s - %(name)s :: %(line)s - %(levelname)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = RotatingFileHandler(filename="/tmp/worker.log", maxBytes=2, backupCount=2) 
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.WARNING)
    logger.addHandler(sh)
    logger.addHandler(fh)

def init_bot_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s - %(name)s :: %(line)s - %(levelname)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = RotatingFileHandler(filename="/tmp/worker.log", maxBytes=2, backupCount=2) 
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(fh)