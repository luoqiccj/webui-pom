#coding=utf-8
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import unittest
from utils.HTMLTestRunner import HTMLTestRunner
from datetime import datetime
from utils.get_info import log
from utils.get_info import get_project_dir
import platform
from utils.get_config_data import GetConfigData

class RunMain(unittest.TestCase):
    #获取所有测试用例
    def get_all_testcase(self):
        dir_name = os.path.abspath(os.path.dirname(os.getcwd()))
        test_case_dir = os.path.join(dir_name,"TestCase")
        log.info("test_case_dir=%s"%test_case_dir)
        ts = unittest.defaultTestLoader.discover(test_case_dir,"*Test.py")
        return ts

    def set_report_name(self):
        broswer_type = sys.argv[1]
        day = datetime.now().strftime("%Y%m%d")
        case_name = os.path.basename(__file__).split(".")[0]
        # dir_name = os.path.abspath(os.path.dirname(os.getcwd())) + "\\Report"
        dir_name = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),"Report",day)
        log.info("dir_name=%s"%dir_name)
        file_exist = os.path.exists(dir_name)
        log.info("file_exist=%s"%file_exist)
        if not file_exist:
            os.makedirs(dir_name)
        else:
            log.info("dir_name = %s文件夹已存在"%dir_name)
        file_name = "report_" + case_name + "_" + day + "("+ broswer_type + ")" +".html"
        report_name = os.path.join(dir_name, file_name)
        log.info("report_name = %s" % report_name)
        return report_name

    #获取case_list.txt中设定的用例
    def get_case_list(self):
        cur_dir = os.path.os.getcwd()
        file_name = os.path.join(cur_dir,"case_list.txt")
        fp = open(file_name)
        case_list=[]
        for case in fp.readlines():
            log.info("case=%s"%case)
            if case !='' and not case.startswith("#"):
                case_list.append(case.replace("\n",""))
        log.info("case_list=%s",case_list)
        fp.close()
        return case_list

    #根据case_list设定测试套件
    def get_case_suit(self):
        #定义测试套件
        test_suit = unittest.TestSuite()
        #获取case_list设定的用例
        case_list=self.get_case_list()
        #获取测试用例路径
        dir_name = os.path.abspath(os.path.dirname(os.getcwd()))
        test_case_dir = os.path.join(dir_name, "TestCase")
        log.info("test_case_dir=%s" % test_case_dir)
        st = []
        #查找出case_list中设定的用例文件
        for case in case_list:
            discover = unittest.defaultTestLoader.discover(test_case_dir, case)
            st.append(discover)
        # 把case_list设定的用例文件中的测试用例添加到测试套件中
        for suit in st:
            for test_name in suit:
                test_suit.addTest(test_name)

        return test_suit

    def run_main(self,run_case_type=None):
        #系统版本
        plat = platform.system()
        plat_ver = platform.version()
        log.info("plat_ver = %s"%plat_ver)

        #根据参数 获取测试套件
        if run_case_type=='2':
            ts = self.get_case_suit()
        elif run_case_type =='1' or run_case_type==None:
            ts = self.get_all_testcase()
        else:
            log.info("用例范围参数错误，应该为空，1,2")
        report_name = self.set_report_name()
        # 打开report.html文件
        fp = open(report_name, "wb")
        #执行用例
        runner = HTMLTestRunner(fp, title="WEBUI自动化测试报告",
                                description="环境：%s %s   浏览器：%s"%(plat,plat_ver,sys.argv[1]))
        result = runner.run(ts)

        option = "%s_success_count" % sys.argv[1]
        self.write_ini_file("count",option,result.success_count)

        option = "%s_failure_count" % sys.argv[1]
        self.write_ini_file("count", option, result.failure_count)

        option = "%s_error_count" % sys.argv[1]
        self.write_ini_file("count", option, result.error_count)
        #关闭文件句柄
        fp.close()

    #写data.ini文件
    def write_ini_file(self,section,option,value):
        filename = os.path.join(get_project_dir(),"ConfigFile","data.ini")
        cf = GetConfigData(filename)
        #option = "%s_success_count" % sys.argv[1]
        cf.add_setion(section)
        cf.add_option(section,option, str(value))
        cf.write_ini()

if __name__ == '__main__':
    gp = GlobalParam()
    gp.set_value("ie","ie")
    log.info(gp.get_value("ie"))

    if len(sys.argv) == 3:
        RunMain().run_main(sys.argv[2])
    elif len(sys.argv) == 2:
        RunMain().run_main()
    else:
        log.info("参数个数错误")




