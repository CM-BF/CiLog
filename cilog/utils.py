"""
FileName: utils.py
Description: 
Time: 2020/9/11 17:42
Project: CiLog
Author: Shurui Gui
"""
import re
import sys
import copy


def construct_mark(left_string: str):
    mark = f'[{left_string[0].lower()}{left_string[0].upper()}]'
    left_string = left_string[1:]

    if left_string:
        mark += f'({construct_mark(left_string)})?'

    return mark


def str2mark(string):

    return f'#{construct_mark(string)}#'


class CiLogStdOut(object):

    def __init__(self, logger):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self
        self.logger = logger

    def write(self, string):

        if string == '\n':
            return

        for level in ['debug', 'important', 'warning', 'error', 'critical', 'mail']:
            match = re.match(str2mark(level), string)
            if match:
                getattr(self.logger, level)(string[match.span()[1]:])
                return

        self.logger.info(string)

    def flush(self):
        return


