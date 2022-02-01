"""
FileName: table_test.py
Description: 
Time: 2021/1/10 15:17
Project: CiLog
Author: Shurui Gui
"""

from cilog import fill_table


table_format = [['A', 'B', 'C', 'H', 'E', 'F', 'G', 'D'],
                ['da', 'db', 'dc', 'de'],
                ['sa', 'sb', 'sc', 'sd', 'sf']]

fill_table('./excel_test.xlsx', value='0.4013', x='D', y='db', z='sd', table_format=table_format)