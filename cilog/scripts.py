"""
FileName: scripts.py
Description: 
Time: 2020/9/12 12:06
Project: CiLog
Author: Shurui Gui
"""

import argparse
import subprocess
import signal
import sys, os
from cilog.api import create_logger, json_mail_setting
import json
import shutil
from definitions import ROOT_DIR



def signal_process():
    os.setsid()
    # signal.signal(signal.SIGHUP, signal.SIG_IGN)

parser = argparse.ArgumentParser()
parser.add_argument('-c', type=str, default='~/.cilog/config.json', help='Config file')
parser.add_argument('-r', type=str, default='./cilog.log', help='Output redirection')
parser.add_argument('-e', action='store_true', default=False, help='Set enable_mail to True.')
parser.add_argument('cmd', nargs='+')
args = parser.parse_known_args()

config_filename = os.path.abspath(os.path.expanduser(args[0].c))
default_config = os.path.abspath(os.path.expanduser('~/.cilog/config.json'))
redirect_filename = os.path.abspath(os.path.expanduser(args[0].r))

print(f'Output -> {redirect_filename}')

if not os.path.exists(config_filename):
    if config_filename == default_config:
        os.makedirs(os.path.dirname(default_config))

        shutil.copy(os.path.join(ROOT_DIR, 'config.json'),
                    default_config)
        print(f'\nDefault config file does not exist.\n'
              f'-------------------------------------\n'
              f'{default_config} is automatically added, please configure it!')
        exit(0)
    else:
        raise FileNotFoundError(f'Config file {config_filename} Not Found.')


with open(config_filename, 'r') as f:
    config = json.load(f)
    logger = create_logger(name=config['log_name'], file=args[0].r, use_color=False, enable_mail=args[0].e,
                           mail_setting=json_mail_setting(config['mail_setting']))


cmd = args[0].cmd + args[1]

process = subprocess.Popen(cmd, preexec_fn=signal_process, stdout=open(redirect_filename, 'a'), stderr=subprocess.STDOUT)

process.wait()
logger.mail(f'Task {" ".join(cmd)} completed.')






