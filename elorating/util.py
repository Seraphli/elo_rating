import logging


def get_path(name='log', abspath=None, relative_path=None,
             _file=None, parent=False):
    """Create path if path don't exist
    Args:
        name: folder name
        abspath: absolute path to be prefix
        relative_path: relative path that can be convert into absolute path
        _file: use directory based on _file
        parent: whether the path is in the parent folder
    Returns: Path of the folder
    """
    import os
    if abspath:
        directory = os.path.abspath(os.path.join(abspath, name))
    elif relative_path:
        directory = os.path.abspath(os.path.join(
            os.path.abspath(relative_path), name))
    else:
        if _file:
            if parent:
                directory = os.path.abspath(
                    os.path.join(os.path.dirname(_file), os.pardir, name))
            else:
                directory = os.path.abspath(
                    os.path.join(os.path.dirname(_file), name))
        else:
            if parent:
                directory = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), os.pardir, name))
            else:
                directory = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), name))
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = '\033[0m'
COLOR_SEQ = '\033[1;%dm'
BOLD_SEQ = '\033[1m'
COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED,
    'RED': RED,
    'GREEN': GREEN,
    'YELLOW': YELLOW,
    'BLUE': BLUE,
    'MAGENTA': MAGENTA,
    'CYAN': CYAN,
    'WHITE': WHITE,
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):
        levelname = record.levelname
        if levelname in COLORS:
            levelname_color = COLOR_SEQ % (
                    30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        message = logging.Formatter.format(self, record)
        message = message.replace('$RESET', RESET_SEQ) \
            .replace('$BOLD', BOLD_SEQ)
        for k, v in COLORS.items():
            message = message.replace('$' + k, COLOR_SEQ % (v + 30)) \
                .replace('$BG' + k, COLOR_SEQ % (v + 40)) \
                .replace('$BG-' + k, COLOR_SEQ % (v + 40))
        return message + RESET_SEQ


def init_logger(name, path=None, level=(logging.DEBUG, logging.INFO)):
    """Initialize a logger with certain name
    Args:
        name (str): Logger name
        path (str): Optional, specify which folder path
            the log file will be stored, for example
            '/tmp/log'
        level (tuple): Optional, consist of two logging level.
            The first stands for logging level of file handler,
            and the second stands for logging level of console handler.
    Returns:
        logging.Logger: logger instance
    """
    import logging.handlers
    import sys
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = 0
    _nf = ['[%(asctime)s]',
           '[%(name)s]',
           '[%(filename)20s:%(funcName)15s:%(lineno)5d]',
           '[%(levelname)s]',
           ' %(message)s']
    _cf = ['$GREEN[%(asctime)s]$RESET',
           '[%(name)s]',
           '$BLUE[%(filename)20s:%(funcName)15s:%(lineno)5d]$RESET',
           '[%(levelname)s]',
           ' $CYAN%(message)s$RESET']
    nformatter = logging.Formatter('-'.join(_nf))
    cformatter = ColoredFormatter('-'.join(_cf))

    if path:
        path += '/' + name + '.log'
    else:
        path = get_path('log') + '/' + name + '.log'

    rf = logging.handlers.RotatingFileHandler(path, maxBytes=50 * 1024 * 1024,
                                              backupCount=5)
    rf.setLevel(level[0])
    rf.setFormatter(nformatter)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level[1])
    ch.setFormatter(cformatter)

    logger.addHandler(rf)
    logger.addHandler(ch)
    return logger


import datetime


def get_run_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


RUN_TIMESTAMP = get_run_timestamp()


class DummyLogger(object):
    """Dummy logger, replace all method with pass"""

    def __init__(self):
        pass

    def setLevel(self, level):
        pass

    def debug(self, msg, *args, **kwargs):
        pass

    def info(self, msg, *args, **kwargs):
        pass

    def warning(self, msg, *args, **kwargs):
        pass

    def warn(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass

    def exception(self, msg, *args, exc_info=True, **kwargs):
        pass

    def critical(self, msg, *args, **kwargs):
        pass

    fatal = critical

    def log(self, level, msg, *args, **kwargs):
        pass

    def findCaller(self, stack_info=False):
        pass

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        pass

    def _log(self, level, msg, args, exc_info=None, extra=None,
             stack_info=False):
        pass

    def handle(self, record):
        pass

    def addHandler(self, hdlr):
        pass

    def removeHandler(self, hdlr):
        pass

    def hasHandlers(self):
        pass

    def callHandlers(self, record):
        pass

    def getEffectiveLevel(self):
        pass

    def isEnabledFor(self, level):
        pass

    def getChild(self, suffix):
        pass


class Dummytqdm(object):
    def update(self, n=1):
        pass

    def close(self):
        pass

    def unpause(self):
        pass

    def set_description(self, desc=None, refresh=True):
        pass

    def set_description_str(self, desc=None, refresh=True):
        pass

    def set_postfix(self, ordered_dict=None, refresh=True, **kwargs):
        pass

    def set_postfix_str(self, s='', refresh=True):
        pass

    def moveto(self, n):
        pass

    def clear(self, nolock=False):
        pass

    def refresh(self, nolock=False):
        pass
