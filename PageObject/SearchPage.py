#coding=utf-8
from BasePage.BasePage import BasePage
from PageObject.LoginPage import LoginPage
from utils.get_info import log
from utils.get_config_data import GetConfigData
from time import sleep
from utils.get_db_data import GetDBData

class SearchPage(BasePage):
    # 登录系统
    def login_sys(self,broswer_type=None):
        self.cf = GetConfigData()
        self.lp = LoginPage()
        self.lp.open_login_page(broswer_type)
        # 获取账号密码
        usr = self.cf.get_data("login", "login_usr")
        psw = self.cf.get_data("login", "login_psw")
        self.lp.login(usr, psw)
        return self.lp.driver

    def open_search_page(self,broswer_type=None):
        #登录
        self.driver = self.login_sys(broswer_type)
        #search页面url
        self.link = self.cf.get_data("test_env", "url")
        url = self.link + "#/search"
        # 打开search页面
        self.driver.get(url)


    def click_search_button(self):
        self.click_element("xpath",'//*[@id="app"]/div/div[2]/form[2]/div[2]/div/button')

    def search_one_company(self,value=None):
        self.send_text("xpath",'//*[@id="app"]/div/div[2]/form[1]/div[1]/div/div/div[1]/input',value)
        self.click_search_button()

    def history_search(self):
        pass

    def my_forcus(self):
        pass

    def high_search(self):
        pass

    #获取数据库的公司记录数
    def get_db_company_count(self):
        db = GetDBData()
        sql = "select count(distinct company_id) from b_rpt_report r where  r.report_type='1';"
        data = db.select_db(sql)
        log.info("db data=%s"%data)
        return int(data[0][0])

    # 获取页面的公司记录数
    def get_page_company_count(self):
        element = self.find_element("xpath",'//*[@id="app"]/div/div[3]/div[1]')
        count = element.text.split(" ")[1]
        log.info("count=%s" %count)
        return int(count)

    def view_report(self):
        try:
            #点击查看报告/查看按钮
            self.click_element("xpath", '//*[@id ="app"]/div/div[3]/div[2]/div[1]/div[1]/div[1]/div[3]/button/span')
            log.info("click view_report btn")
            self.click_element("xpath", '//*[@id="app"]/div/div[3]/div[2]/div[1]/div[1]/div[2]/table/tr[1]/td[5]/button/span')
            log.info("click view  btn")
            #获取当前窗口句柄
            cur_handle = self.lp.driver.current_window_handle
            log.info("cur_handle=%s" % cur_handle)
            # 获取所有窗口句柄
            handles = self.lp.driver.window_handles
            log.info("handles=%s"%handles)
            # 切换到新的报告查看页面
            for handle in handles:
                if handle != cur_handle:
                    self.lp.driver.switch_to.window(handle)
            cur_handle = self.lp.driver.current_window_handle
            log.info("cur_handle2=%s" % cur_handle)
            #查找新标签页上的元素
            element = self.find_element("xpath",'//*[@id="publicOpinionAlert"]/div[1]')
            log.info("element=%s"%element)
        except:
            log.info("can not find element")


if __name__ == '__main__':
    sp = SearchPage()
    sp.open_search_page()

    sp.search_one_company(" ")
    sp.view_report()
    # sp.get_db_company_count()
    # sp.get_page_company_count()
    sleep(3)
    sp.close_broswer()



