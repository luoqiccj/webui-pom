#coding=utf-8
from PageObject.LoginPage import LoginPage
import unittest
from time import sleep
from ddt import ddt,data,unpack
from utils.get_info import log
from utils.HTMLTestRunner import HTMLTestRunner
from datetime import datetime
import os
import sys
from utils.get_excel_data import GetExcelData
excel = GetExcelData()
excel.open_excel_file()

@ddt
class LoginTest(unittest.TestCase):
    #类前置条件，一个类只执行一次
    @classmethod
    def setUpClass(cls):
        broswer_type = sys.argv[1]
        log.info("broswer_type=%s" % broswer_type)
        cls.lp = LoginPage()
        cls.lp.open_login_page(broswer_type)


    # 用例前置条件，每条用例都会执行
    def setUp(self):
        # broswer_type = sys.argv[1]
        # log.info("broswer_type=%s" % broswer_type)
        # self.lp = LoginPage()
        # self.lp.open_login_page(broswer_type)
        pass

    # 类后置条件，一个类只执行一次
    @classmethod
    def tearDownClass(cls):
        sleep(3)
        #关闭浏览器
        cls.lp.close_broswer()

    # 用例后置处理
    def tearDown(self):
        # sleep(3)
        # #关闭浏览器
        # self.lp.close_broswer()
        pass

    #数据驱动测试登录
    @data(("nbyh_admin", "123456"), ("nbyh_admin", "1234567"))
    @unpack
    def test_1(self,username,password):
        self.lp.login(username,password)
        log.info(unittest.TestCase.id(self).split(".")[2].split("___")[0])
        #根据每个用例设定断言
        #第一个用例 登录成功
        if unittest.TestCase.id(self).split(".")[2].split("___")[0] == "test_1_1":
            result = self.lp.get_login_success_element()
            self.assertTrue(result)
        # 第二个用例 登录失败，提示用户名密码错误
        elif unittest.TestCase.id(self).split(".")[2].split("___")[0] == "test_1_2":
            error = self.lp.get_username_or_password_error()
            self.assertTrue(error)

    # excel数据驱动测试登录
    @data(*excel.get_all_row_data())
    @unpack
    def test_2(self, username, password):
        self.lp.login(username, password)
        log.info(unittest.TestCase.id(self).split(".")[2].split("___")[0])
        # 根据每个用例设定断言
        # 第一个用例 登录成功
        if unittest.TestCase.id(self).split(".")[2].split("___")[0] == "test_2_1":
            result = self.lp.get_login_success_element()
            self.assertTrue(result)
        # 第二个用例 登录失败，提示用户名密码错误
        elif unittest.TestCase.id(self).split(".")[2].split("___")[0] == "test_2_2":
            error = self.lp.get_username_or_password_error()
            self.assertTrue(error)

        # 第三个用例 登录失败，提示请输入密码
        elif unittest.TestCase.id(self).split(".")[2].split("___")[0] == "test_2_3":
            error = self.lp.get_input_psw_tips()
            self.assertTrue(error)

        # 第四个用例 登录失败，提示请输入用户名
        elif unittest.TestCase.id(self).split(".")[2].split("___")[0] == "test_2_4":
            error = self.lp.get_input_usr_tips()
            self.assertTrue(error)

    def test_3(self):
        self.lp.login("nbyh_admin","123456")
        result = self.lp.get_login_success_element()
        log.info("result = %s"%result)
        self.assertTrue(result)


if __name__ == '__main__':
    # unittest.main()
    ts = unittest.TestSuite()
    #添加用例
    ts.addTest(LoginTest("test_3"))
    # 添加所有用例
    case_dir_name = os.path.abspath(os.path.dirname(os.getcwd())) + "/TestCase"
    discover = unittest.defaultTestLoader.discover(case_dir_name,"LoginTest.py")
    #获取当前日期
    # day = datetime.now().strftime("%Y%m%d_%H%M%S")
    day = datetime.now().strftime("%Y%m%d")
    #获取用例名称，去掉.py
    case_name = os.path.basename(__file__).split(".")[0]
    dir_name = os.path.abspath(os.path.dirname(os.getcwd())) +"/Report"
    file_name = "report_" + case_name +"_"+  day+".html"
    report_name = os.path.join(dir_name,file_name)
    log.info("report_name = %s"%report_name)
    #打开report.html文件
    fp = open(report_name,"wb")
    runner =  HTMLTestRunner(fp)
    # runner.run(ts)
    runner.run(discover)
    fp.close()

