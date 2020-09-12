"""
FileName: launcher.py
Description: 
Time: 2020/9/12 13:15
Project: CiLog
Author: Shurui Gui
"""
import sys, subprocess, signal, os

sys_argv = sys.argv

def signal_process():
    # os.setsid()
    signal.signal(signal.SIGHUP, signal.SIG_IGN)

def launcher():
    subprocess.Popen(['python',
                      os.path.join(os.path.dirname(__file__), 'scripts.py'),
                      *sys_argv[1:]], preexec_fn=signal_process)

