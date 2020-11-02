"""
FileName: formatter.py
Description: 
Time: 2020/9/11 16:41
Project: CiLog
Author: Shurui Gui
"""

import logging
from traceback import extract_stack, StackSummary



RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
COLORS = {
    'WARNING': YELLOW,
    'IMPORTANT': CYAN,
    'MAIL': CYAN,
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
        self.msg_fmt = msg_fmt or \
            {
                'ORIGIN': "%(message)s",
                'DEBUG': "%(levelname)s: %(asctime)s : $BOLD%(message)s$RESET",
                'INFO': "%(levelname)s: $BOLD%(message)s$RESET",
                'WARNING': "%(levelname)s: %(filename)s - line %(lineno)d : $BOLD%(message)s$RESET",
                'IMPORTANT': "%(levelname)s: %(asctime)s : $BOLD%(message)s$RESET",
                'ERROR': "%(levelname)s: %(asctime)s - %(filename)s - line %(lineno)d : $BOLD%(message)s$RESET",
                'CRITICAL': "%(levelname)s: %(asctime)s - %(filename)s - line %(lineno)d : $BOLD%(message)s$RESET",
                'MAIL': "%(levelname)s: %(asctime)s : $BOLD%(message)s$RESET"
            }
        for key in self.msg_fmt.keys():
            self.msg_fmt[key] = bold_msg(self.msg_fmt[key], self.use_color)

    def format(self, record) -> str:

        # set for different levels
        format_orig = self._style._fmt
        self._style._fmt = self.msg_fmt[record.levelname]

        # preprocess \n
        line_count = 0
        for s in record.msg:
            if s == '\n':
                line_count += 1
                record.msg = record.msg[1:]
            else:
                break
        if record.msg:
            self._style._fmt = line_count * '\n' + self._style._fmt
        else:
            self._style._fmt = line_count * '\n'

        if record.levelno >= self.stack_level and record.levelno != logging.MAIL:
            record.stack_info = ''.join(StackSummary.from_list(extract_stack()[:self._stack_prune]).format())

        # make it colorful
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + record.levelname + RESET_SEQ
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