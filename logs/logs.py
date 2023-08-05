import logging

def init_worker_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s - %(name)s :: %(line)s - %(levelname)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler('/tmp/test.log')
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.WARNING)
    logger.addHandler(sh)
    logger.addHandler(fh)

def init_block_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s - %(name)s :: %(line)s - %(levelname)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler('/tmp/blocks.log')
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(fh)

def init_bot_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s - %(name)s :: %(line)s - %(levelname)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler('/tmp/bot.log')
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(fh)