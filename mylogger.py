import inspect
import logging

SIMPLEFORMAT = '[%(name)s] %(message)s'
FULLFORMAT = '%(asctime)s - %(levelname)s - [%(name)s] - %(message)s'

def getLogger(**kwargs):
    caller = kwargs['name'] if 'name' in kwargs else inspect.stack()[1][1].split('/')[-1]

    logger = logging.getLogger(caller)
    logger.setLevel(kwargs['level'] if 'level' in kwargs else logging.WARNING)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    format = kwargs['format'] if 'format' in kwargs else SIMPLEFORMAT
    formatter = logging.Formatter(format)

    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger