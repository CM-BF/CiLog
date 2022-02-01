"""
FileName: test3.py
Description: 
Time: 2020/9/12 19:21
Project: CiLog
Author: Shurui Gui
"""
from cilog import create_logger
from tqdm import tqdm
from time import sleep
create_logger(sub_print=True)
# print('#E#input')
# for i in tqdm(range(10)):
#     sleep(1)
#     print(i)
raise Exception('abc')
# import sys, traceback
# # sys.stderr.write('abc\n')
# print(traceback.extract_stack())
# def fun():
#     print(traceback.extract_stack())
#
# fun()
# for i in tqdm(range(10)):
#     print(f'#IN#{i}')