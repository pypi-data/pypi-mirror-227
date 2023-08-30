import logging
import os
from neco_f.os_time import get_date
import file_tools


def setup(dir_name='Logs', file_name=get_date(),
          file_mode='a'):
    file_tools.mkdir(dir_name)
    if len(os.listdir(dir_name)) >= 15:
        file_tools.del_dir(dir_name, mode=1)
        print('成功清理日志')

    work_dir = f'{dir_name}/{file_name}.log'.replace('/', '\\')
    logging.basicConfig(filename=work_dir,
                        format='%(asctime)s %(message)s',
                        level=logging.INFO,
                        filemode=file_mode,
                        encoding='utf-8')


def info(msg):
    logging.info(msg)
# setup()