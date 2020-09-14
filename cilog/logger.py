"""
FileName: logger.py
Description: 
Time: 2020/7/28 15:18
Project: CiLog
Author: Shurui Gui
"""

import logging
import re
import sys
import builtins
from functools import partial
from cilog.utils import CiLogStdOut


logging.IMPORTANT = 35
logging.MAIL = 60

s2l = {
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'IMPORTANT': logging.IMPORTANT,
    'MAIL': logging.MAIL,
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'NOTSET': logging.NOTSET
}

logging.addLevelName(logging.IMPORTANT, 'IMPORTANT')
logging.addLevelName(logging.MAIL, 'MAIL')


# ------------------------------ set new levels --------------------------------
class CustomLogger(logging.Logger):
    print = builtins.print

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level=logging.NOTSET)

    def important(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'IMPORTANT'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "major disaster", exc_info=1)
        """
        if self.isEnabledFor(logging.IMPORTANT):
            self._log(logging.IMPORTANT, msg, args, **kwargs)

    def mail(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'MAIL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "major disaster", exc_info=1)
        """
        if self.isEnabledFor(logging.MAIL):
            self._log(logging.MAIL, msg, args, **kwargs)

    def substitute_print(self):

        builtins.print = print_flush

        return CiLogStdOut(self)

    def restore_print(self):

        builtins.print = CustomLogger.print

        return

def print_flush(*values, sep=' ', end='\n', file=None, flush=True):
    sys.stdout.flush()
    CustomLogger.print(*values, sep=sep, end=end, file=file, flush=flush)

        # def log_print(*values, sep=' ', end='\n', file=sys.stdout, flush=False):
        #     if end != '\n' or file != sys.stdout or flush != False:
        #         builtins.print(values, sep=sep, end=end, file=file, flush=flush)
        #         return
        #
        #     for level in ['debug', 'important', 'warning', 'error', 'critical', 'mail']:
        #         match = re.match(str2mark(level), values[0])
        #         if match:
        #             getattr(self, level)(sep.join([str(value) for value in values])[match.span()[1]:])
        #             return
        #
        #     self.info(sep.join([str(value) for value in values]))
        #
        # return log_print





