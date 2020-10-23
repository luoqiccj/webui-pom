#coding=utf-8
from PageObject.SearchPage import SearchPage
import unittest
from time import sleep
from ddt import ddt,data,unpack
from utils.get_info import log
from utils.HTMLTestRunner import HTMLTestRunner
from datetime import datetime
import os
import sys

class SearchTest(unittest.TestCase):
    #每个用例执行前，打开search页面
    def setUp(self):
        self.sp = SearchPage()
        broswer_type = sys.argv[1]
        log.info("broswer_type=%s" % broswer_type)
        self.sp.open_search_page(broswer_type)
        self.driver = self.sp.driver

    #测试用例，搜索单个公司
    def test_search_one_company(self):
        self.sp.search_one_company("厦门建发股份有限公司")

    # @unittest.skip
    # 测试用例，搜索所有公司
    def test_search_all_company(self):
        self.sp.click_search_button()
        page_company_count = self.sp.get_page_company_count()
        db_company_count = self.sp.get_db_company_count()
        log.info("page_company_count=%s,db_company_count=%s"%(page_company_count,db_company_count))
        self.assertEqual(page_company_count,db_company_count)

    #用例执行后操作，关闭浏览器
    def tearDown(self):
        self.sp.close_broswer()

if __name__ == '__main__':
    # unittest.main()
    ts = unittest.TestSuite()
    #添加用例
    ts.addTest(SearchTest("test_search_one_company"))
    ts.addTest(SearchTest("test_search_all_company"))
    #获取当前日期
    # day = datetime.now().strftime("%Y%m%d_%H%M%S")
    day = datetime.now().strftime("%Y%m%d")
    case_name = os.path.basename(__file__).split(".")[0]
    dir_name = os.path.abspath(os.path.dirname(os.getcwd())) +"/Report"
    file_name = "report_" + case_name +"_"+  day+".html"
    report_name = os.path.join(dir_name,file_name)
    log.info("report_name = %s"%report_name)
    #打开report.html文件
    fp = open(report_name,"wb")
    runner =  HTMLTestRunner(fp)
    runner.run(ts)
    fp.close()





