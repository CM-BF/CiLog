"""
FileName: logger.py
Description: 
Time: 2020/7/28 15:18
Project: CiLog
Author: Shurui Gui
"""


import logging
from traceback import extract_stack, print_list, StackSummary


s2l = {
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR
}


RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': MAGENTA,
    'ERROR': RED
}


def bold_msg(message, use_color):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


class CustomFormatter(logging.Formatter):

    def __init__(self, use_color, stack_level, msg_fmt=None, file=False):
        super().__init__("%(levelno)s: %(msg)s")
        self.use_color = use_color if not file else False
        self.stack_level = stack_level
        self._stack_prune = -8 if not file else -9
        self.msg_fmt = msg_fmt if msg_fmt != None else \
            {
            'DEBUG': "%(levelname)s: %(asctime)s : $BOLD%(message)s$RESET",
            'INFO': "%(levelname)s: $BOLD%(message)s$RESET",
            'WARNING': "%(levelname)s: %(filename)s - line %(lineno)d : $BOLD%(message)s$RESET",
            'ERROR': "%(levelname)s: %(asctime)s - %(filename)s - line %(lineno)d : $BOLD%(message)s$RESET",
            'CRITICAL': "%(levelname)s: %(asctime)s : $BOLD%(message)s$RESET"
        }
        for key in self.msg_fmt.keys():
            self.msg_fmt[key] = bold_msg(self.msg_fmt[key], self.use_color)


    def format(self, record) -> str:

        # set for different levels
        format_orig = self._style._fmt
        self._style._fmt = self.msg_fmt[record.levelname]
        if record.levelno >= self.stack_level:
            record.stack_info = ''.join(StackSummary.from_list(extract_stack()[:self._stack_prune]).format())

        # make it colorful
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color

        self.datefmt = '%m/%d/%Y %I:%M:%S %p'
        result = logging.Formatter.format(self, record)

        self._style._fmt = format_orig
        record.levelname = levelname

        return result


class FileFormatter(CustomFormatter):

    def __init__(self, stack_level, msg_fmt=None):
        __file = True
        __use_color = False
        super().__init__(__use_color, stack_level, msg_fmt=msg_fmt, file=__file)


def create_logger(**kwargs) -> logging.Logger:
    """
    Create logger for logging
    :param Require[name] : str - logger name
    :param Optional[file] : str - File path
    :param Optional[file_mode] : str - File open mode. Default: 'a'
    :param Optional[file_level] : Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] - Default 'INFO'
    :param Optional[use_color] : bool - Signal for using colored info. Default False
    :param Optional[stack_level] : Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] - Default 'ERROR'
    :param Optional[msg_fmt] : Dict{'DEBUG': debug_fmt, 'INFO': info_fmt, 'WARNING': warning_fmt,
    'ERROR': error_fmt, 'CRITICAL': critical_fmt} - Custom design massage format.
    Please refer to CustomFormatter and url: https://docs.python.org/3/library/logging.html#logrecord-attributes
    :return: logger : logging.Logger
    """

    if 'name' not in kwargs.keys():
        raise Exception('param [name] must be specified.')

    if 'file_level' not in kwargs.keys():
        kwargs['file_level'] = 'INFO'

    if 'use_color' not in kwargs.keys():
        kwargs['use_color'] = False

    if 'file_mode'  not in kwargs.keys():
        kwargs['file_mode'] = 'a'

    if 'stack_level' not in kwargs.keys():
        kwargs['stack_level'] = 'ERROR'

    kwargs['file_level'] = s2l[kwargs['file_level']]
    kwargs['stack_level'] = s2l[kwargs['stack_level']]


    # create logger
    logger = logging.getLogger(kwargs['name'])
    logger.setLevel(logging.DEBUG)

    # console handler and its formatter
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    cformatter = CustomFormatter(use_color=kwargs['use_color'],
                                 stack_level=kwargs['stack_level'])
    ch.setFormatter(cformatter)
    logger.addHandler(ch)

    # file handler
    if 'file' in kwargs.keys():
        fh = logging.FileHandler(kwargs['file'], mode=kwargs['file_mode'])
        fh.setLevel(kwargs['file_level'])
        fformatter = FileFormatter(stack_level=kwargs['stack_level'])
        fh.setFormatter(fformatter)
        logger.addHandler(fh)

    return logger



