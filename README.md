# CiLog

CiLog is a flexible integrated logging tool with color and custom bold font base on package logging.

## Feature

* colored console outputs
* setting stack info output level
* easier way to custom format for each level

## Install

```bash
$ pip install cilog
```

## Basic Usage

```python
from cilog.logger import create_logger


def call_error():
    logger.error('Exception')

logger = create_logger(name='l1', file='./log.log', use_color=True, ipt_info=True)
logger.info('start')
logger.debug('here')
logger.warning('warn')
call_error()
logger.critical('Program exit.')
```

-- Result:
![result](https://github.com/CM-BF/CiLog/blob/master/result.png)

`create_logger` keywords:

Optional[**file**] : str - File path. Specify to log into a file.

Optional[**file_mode**] : str - File open mode. Default: 'a'

Optional[**file_level**] : Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] - Default 'INFO'

Optional[**use_color**] : bool - Signal for using colored info. Default False

Optional[**stack_level**] : Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] - Default 'ERROR'

**(New feature)** Optional[ipt_info]: bool - Signal for using CRITICAL as important massage without stack_info.

Optional[**msg_fmt**] : Dict{'DEBUG': debug_fmt, 'INFO': info_fmt, 'WARNING': warning_fmt,
'ERROR': error_fmt, 'CRITICAL': critical_fmt} - Custom design massage format. 
(Specially, you can use $BOLD **text** $RESET to use bold font)
Please refer to CustomFormatter and url: https://docs.python.org/3/library/logging.html#logrecord-attributes

return: logger : logging.Logger

## LICENSE

See [MIT LICENSE](https://github.com/CM-BF/CiLog/blob/master/LICENSE)
