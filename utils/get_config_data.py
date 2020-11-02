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
            self.filepath= os.path.join(pj_dir,"ConfigFile","config.ini")
            # print("__init__ filepath = %s" %filepath)
        else:
            self.filepath=filepath
        #读取指定路径的ini文件
        self.cp.read(self.filepath)

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

    #新增一个section
    def add_setion(self,section):
        print("self.cp.has_section(section) = %s" %self.cp.has_section(section))
        if not self.cp.has_section(section):
            self.cp.add_section(section)

    #section里面新增key和value
    def add_option(self,section,option,value):
        print("self.cp.has_option(section,option) = %s" % self.cp.has_option(section,option))
        if  self.cp.has_option(section,option):
            self.cp.remove_option(section, option)
        self.cp.set(section, option, value)

    #写ini文件
    def write_ini(self):
        fp = open(self.filepath,"w")
        self.cp.write(fp)
        fp.close()

if __name__ == '__main__':
    cf = GetConfigData()
    data = cf.get_data("test_env","url")
    cf.add_setion("test")
    print(data)


