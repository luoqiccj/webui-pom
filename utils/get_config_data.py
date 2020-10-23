#coding=utf-8
from configparser import ConfigParser
import os

class GetConfigData:
    def __init__(self,filepath=None):
        self.cp = ConfigParser()
        #获取当前项目工作目录
        pj_dir = self.get_pj_dir()

        #未传入filepath参数，则默认赋值当前项目工作目录下的ConfigFile/config.ini
        if filepath==None:
            filepath= os.path.join(pj_dir,"ConfigFile","config.ini")
            # print("__init__ filepath = %s" %filepath)
        #读取指定路径的ini文件
        self.cp.read(filepath)

    #获取当前项目工作目录
    def get_pj_dir(self):
        pj_dir = os.path.abspath(os.path.dirname(os.getcwd()))
        # print("__init__ pj_dir = %s" % pj_dir)
        return pj_dir

    #获取ini文件指定模块setion，指定选项option数据
    def get_data(self,setion,option):
        data = self.cp.get(setion,option)
        # print("get_data data = %s" %data)
        return data

if __name__ == '__main__':
    cf = GetConfigData()
    data = cf.get_data("test_env","url")
    print(data)

