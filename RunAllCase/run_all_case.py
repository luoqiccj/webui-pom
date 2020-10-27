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
from utils.send_email import SendMail

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
        dir_name = os.path.abspath(os.path.dirname(os.getcwd())) + "\\Report"
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


if __name__ == '__main__':
    rm = RunMain()
    # sm = SendMail()
    ts = rm.get_case_suit()
    broswer_type = sys.argv[1]
    log.info("broswer_type=%s"%broswer_type)
    report_name = rm.set_report_name()
    # 打开report.html文件
    fp = open(report_name, "wb")
    runner = HTMLTestRunner(fp)
    result = runner.run(ts)
    log.info("success_count=%s" % result.success_count)
    log.info("failure_count=%s" % result.failure_count)
    log.info("error_count=%s" % result.error_count)
    # sm.send_mail(report_name,result.success_count,result.failure_count)
    # sm.close_mail()
    fp.close()

