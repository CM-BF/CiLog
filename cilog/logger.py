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

    def __init__(self, use_color, stack_level, msg_fmt=None, file=False, ipt_info=False):
        super().__init__("%(levelno)s: %(msg)s")
        self.use_color = use_color if not file else False
        self.stack_level = stack_level
        self._stack_prune = -8 if not file else -9
        self.ipt_info = ipt_info
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
        if record.levelno >= self.stack_level and not(self.ipt_info and record.levelno == 50):
            record.stack_info = ''.join(StackSummary.from_list(extract_stack()[:self._stack_prune]).format())

        # make it colorful
        levelname = record.levelname
        if self.ipt_info and record.levelno == 50:
            record.levelname = 'IMPORTANT'
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + record.levelname + RESET_SEQ
            record.levelname = levelname_color

        self.datefmt = '%m/%d/%Y %I:%M:%S %p'
        result = logging.Formatter.format(self, record)

        self._style._fmt = format_orig
        record.levelname = levelname

        return result


class FileFormatter(CustomFormatter):

    def __init__(self, stack_level, msg_fmt=None, ipt_info=False):
        __file = True
        __use_color = False
        super().__init__(__use_color, stack_level, msg_fmt=msg_fmt, file=__file, ipt_info=ipt_info)


def create_logger(**kwargs) -> logging.Logger:
    """
    Create logger for logging
    :param Require[name] : str - logger name
    :param Optional[file] : str - File path
    :param Optional[file_mode] : str - File open mode. Default: 'a'
    :param Optional[file_level] : Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] - Default 'INFO'
    :param Optional[use_color] : bool - Signal for using colored info. Default False
    :param Optional[stack_level] : Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] - Default 'ERROR'
    :param Optional[ipt_info]: bool - Signal for using CRITICAL as important massage without stack_info.
    :param Optional[msg_fmt] : Dict{'DEBUG': debug_fmt, 'INFO': info_fmt, 'WARNING': warning_fmt,
    'ERROR': error_fmt, 'CRITICAL': critical_fmt} - Custom design massage format.
    Please refer to CustomFormatter and url: https://docs.python.org/3/library/logging.html#logrecord-attributes
    :return: logger : logging.Logger
    """

    if not kwargs.get('name'):
        raise Exception('param [name] must be specified.')

    kwargs['file_level'] = s2l[kwargs.get('file_level') or 'INFO']
    kwargs['use_color'] = kwargs.get('use_color') or False
    kwargs['file_mode'] = kwargs.get('file_mode') or 'a'
    kwargs['stack_level'] = s2l[kwargs.get('stack_level') or 'ERROR']
    kwargs['ipt_info'] = kwargs.get('ipt_info') or False


    # create logger
    logger = logging.getLogger(kwargs['name'])
    logger.setLevel(logging.DEBUG)

    # console handler and its formatter
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    cformatter = CustomFormatter(use_color=kwargs['use_color'],
                                 stack_level=kwargs['stack_level'],
                                 ipt_info=kwargs['ipt_info'])
    ch.setFormatter(cformatter)
    logger.addHandler(ch)

    # file handler
    if 'file' in kwargs.keys():
        fh = logging.FileHandler(kwargs['file'], mode=kwargs['file_mode'])
        fh.setLevel(kwargs['file_level'])
        fformatter = FileFormatter(stack_level=kwargs['stack_level'], ipt_info=kwargs['ipt_info'])
        fh.setFormatter(fformatter)
        logger.addHandler(fh)

    return logger



