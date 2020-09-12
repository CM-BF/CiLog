"""
FileName: handler.py
Description: 
Time: 2020/9/11 16:40
Project: CiLog
Author: Shurui Gui
"""
import logging, os, shutil, time


class CustomFileHandler(logging.FileHandler):

    def __init__(self, filename, mode='a', encoding=None, delay=False):
        file = os.path.abspath(os.fspath(filename))
        file_path, file_name_ext = os.path.split(file)
        if os.path.exists(file):
            file_name, file_ext = os.path.splitext(file_name_ext)
            f = open(file, 'r', encoding=encoding)
            if len(f.readlines()) > 1e4:
                f.close()
                shutil.copy(file,
                            os.path.join(file_path,
                                         f'{file_name}-{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}{file_ext}'))
                mode = 'w'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        super().__init__(filename, mode=mode, encoding=encoding, delay=delay)