import logging
import os
from os_time import get_date
import file_tools


def setup(file_name=get_date(),
          file_mode='a'):
    dir_name = 'Logs'
    file_tools.mkdir(dir_name)
    if len(os.listdir(dir_name)) >= 15:
        file_tools.del_dir(dir_name, mode=1)
        print('成功清理日志')

    work_dir = f'{dir_name}/{file_name}.log'
    logging.basicConfig(filename=work_dir,
                        format='%(asctime)s %(message)s',
                        level=logging.INFO,
                        filemode=file_mode,
                        encoding='utf-8')


def info(msg):
    logging.info(msg)
# setup()