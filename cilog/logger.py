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
import os
from cilog.utils import CiLogStdOut
try:
    import pandas
except:
    os.system('pip install pandas --upgrade')
    os.system('pip install tabulate --upgrade')
    import pandas
import ast


logging.ORIGIN = 15
logging.IMPORTANT = 35
logging.TABLELIST = 36
logging.MAIL = 60

s2l = {
    'ORIGIN': logging.ORIGIN,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'IMPORTANT': logging.IMPORTANT,
    'TABLELIST': logging.TABLELIST,
    'MAIL': logging.MAIL,
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'NOTSET': logging.NOTSET
}

logging.addLevelName(logging.ORIGIN, 'ORIGIN')
logging.addLevelName(logging.IMPORTANT, 'IMPORTANT')
logging.addLevelName(logging.TABLELIST, 'TABLELIST')
logging.addLevelName(logging.MAIL, 'MAIL')


# ------------------------------ set new levels --------------------------------
class CustomLogger(logging.Logger):
    print = builtins.print

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level=logging.NOTSET)

    def origin(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ORIGIN'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.origin("Houston, we have a %s", "major disaster", exc_info=1)
        """
        if self.isEnabledFor(logging.ORIGIN):
            self._log(logging.ORIGIN, msg, args, **kwargs)

    def important(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'IMPORTANT'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.important("Houston, we have a %s", "major disaster", exc_info=1)
        """
        if self.isEnabledFor(logging.IMPORTANT):
            self._log(logging.IMPORTANT, msg, args, **kwargs)

    def table_fromlist(self, list_table: list, *args, **kwargs):
        """
        Log 'msg % args' with severity 'TABLELIST'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.table_fromlist(list_table, format)

        list_table: i.e.  [['model', 'dataset1', 'dataset2'],
                           ['m1', value11, value12],
                           ['m2', value21, value22]]
        """
        if self.isEnabledFor(logging.TABLELIST):
            format = 'markdown'
            if isinstance(list_table, str):
                match = re.match('!latex', list_table)
                if match:
                    format = 'latex'
                    list_table = list_table[match.span()[1]:]
                list_table = ast.literal_eval(list_table)

            table_dict = {key: [] for key in list_table[0]}
            for row_index in range(1, len(list_table)):
                row = list_table[row_index]
                for i, key in enumerate(table_dict.keys()):
                    table_dict[key].append(row[i])

            df = pandas.DataFrame(table_dict)

            if format == 'markdown':
                try:
                    table = df.to_markdown(index=False)
                except:
                    print('#W#pandas version too low.')
                    os.system('pip install pandas --upgrade')
                    table = df.to_markdown(index=False)

            if format == 'latex':
                table = df.to_latex(index=False)

            self._log(logging.ORIGIN, table, args, **kwargs)
            self._log(logging.ORIGIN, '\n', args, **kwargs)


    def mail(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'MAIL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.mail("Houston, we have a %s", "major disaster", exc_info=1)
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





