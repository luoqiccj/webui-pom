#coding=utf-8
import logging
import logging.handlers
import datetime
import os
from utils.get_config_data import GetConfigData

class LogConfig:
    def __init__(self):
        #获取配置的日志等级
        cf = GetConfigData()
        level = cf.get_data("log","log_level")
        # print("level=%s"%level)
        #log实例化
        self.lg = logging.getLogger()
        #设置输出级别
        if level=='0':
            log_level=logging.INFO
        elif level=='1':
            log_level=logging.DEBUG
        elif level=='2':
            log_level=logging.WARNING
        else:
            log_level=logging.DEBUG
        self.lg.setLevel(log_level)
        #获取当前日期
        cur_day = datetime.datetime.now().strftime("%Y-%m-%d")
        #获取当前项目工作目录
        cur_dir = os.path.abspath(os.path.dirname(os.getcwd()))
        #定义log文件名称log+当前日期.log
        logfilename = "log" + cur_day +".log"
        #完整的文件名
        filename = os.path.join(cur_dir,"Logs",logfilename)
        #设置按天生成日志文件,最多保留7天
        fh = logging.handlers.TimedRotatingFileHandler(filename,when='D',interval=1,backupCount=7)
        #控制台日志
        sh = logging.StreamHandler()
        #日志输出格式
        formatter = logging.Formatter(fmt="%(asctime)s %(filename)s %(funcName)s %(message)s",
                                      datefmt="%Y/%m/%d %X")


        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        self.lg.addHandler(fh)
        self.lg.addHandler(sh)

if __name__ == '__main__':
    log = LogConfig().lg
    log.info("info")
    log.debug("debug")


