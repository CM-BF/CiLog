"""
FileName: test2.py
Description: 
Time: 2020/9/12 14:34
Project: CiLog
Author: Shurui Gui
"""

from cilog import create_logger


def call_error():
    print('#E#Exception')
    raise('wrong')
'''
mail_setting = {
            mailhost:   string or tuple - YourMailHost or (host, port),
            fromaddr:   string          - YourSenderAddress,
            toaddrs:    list(string)    - List of YourTargetAddresses,
            subject:    string          - Mail Subject,
            credentials:tuple           - (YourUsername, YourPassword),
            secure:     tuple           - () or (KeyfileName) or (KeyfileName, CertificatefileName)
                                            use the secure protocol (TLS),
            timeout:    float           - Default 1.0
        }
'''
mail_setting = {
    'mailhost': ('mail.ustc.edu.cn', 25),
    'fromaddr': 'agnesgsr@mail.ustc.edu.cn',
    'toaddrs': ['707720968@qq.com'],
    'subject': 'CiLog test',
    'credentials': ('agnesgsr@mail.ustc.edu.cn', '19971117')
}
create_logger(name='l1', file='./log.log', use_color=True, enable_mail=True,
                       mail_setting=mail_setting, sub_print=True)
print('origin')
table_list = [['Tox21', 'Clintox'], [1, 2], [3, 4]]
print(f'#t#{table_list}')
print(f'#t#!latex{table_list}')
print('#IN#start')
print('#D#here')
print('#W#warn')
# call_error()
print('#C#Program exit.')
print('#IM#lal')
# logger.mail('test')

