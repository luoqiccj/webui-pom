# coding=utf-8
from datetime import datetime
import os
import sys

from utils.log_config import LogConfig
log = LogConfig().lg


#获取当前日期
def get_cur_date():
    date = datetime.now().strftime("%Y%m%d")
    log.info("date=%s"%date)
    return date

#获取项目工作目录
def get_project_dir():
    dir = os.path.abspath(os.path.dirname(os.getcwd()))
    log.info("dir=%s" % dir)
    return dir


if __name__ == '__main__':
    get_cur_date()
    get_project_dir()
