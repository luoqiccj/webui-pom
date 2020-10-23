#coding=utf-8
from BasePage.BasePage import BasePage
from utils.get_info import log
from utils.get_config_data import GetConfigData
from time import sleep
from utils.get_excel_data import GetExcelData

class LoginPage(BasePage):
    #打开登录页面
    def open_login_page(self,broswer_type = None):
        self.cf = GetConfigData()
        #获取config文件中的url
        self.link = self.cf.get_data("test_env","url")
        #打开浏览器
        driver = self.open_broswer(broswer_type)
        #拼接指定页面的url
        url = self.link + "#/login"
        #打开指定页面
        self.open_url(driver,url)
        log.info("open url=%s"%url)

    #输入用户
    def input_username(self,value):
        self.send_text("xpath", '//*[@id="app"]/div/form/div[2]/div[2]/div/div[1]/input', value)
        log.info("send text %s" %value)

    #输入密码
    def input_password(self,value):
        self.send_text("xpath", '//*[@id="app"]/div/form/div[2]/div[3]/div/div[1]/input', value)
        log.info("send text %s" %value)

    #点击登录按钮
    def login_button_click(self):
        self.click_element("xpath",'//*[@id="app"]/div/form/div[2]/button')
        log.info("click login button")

    #登录流程
    def login(self,username,password):
        self.input_username(username)
        self.input_password(password)
        self.login_button_click()

    #用户名或密码错误提示
    def get_username_or_password_error(self):
        flag = False
        error_element = self.find_element("xpath",'/html/body/div[2]/p')
        log.info("error_element = %s" % error_element)
        log.info("error_element.text= %s" % error_element.text)
        if error_element.text == "用户密码错误":
            self.get_screenshot()
            flag = True
        return flag

    # 提示”请输入密码“
    def get_input_psw_tips(self):
        flag = False
        error_element = self.find_element("xpath", '//*[@id="app"]/div/form/div[2]/div[3]/div/div[2]')
        log.info("error_element = %s" % error_element)
        log.info("error_element.text= %s" % error_element.text)
        if error_element.text == "请输入密码":
            self.get_screenshot()
            flag = True
        return flag

    # 提示”请输入用户名“
    def get_input_usr_tips(self):
        flag = False
        error_element = self.find_element("xpath", '//*[@id="app"]/div/form/div[2]/div[2]/div/div[2]')
        log.info("error_element = %s" % error_element)
        log.info("error_element.text= %s" % error_element.text)
        if error_element.text == "请输入用户名":
            self.get_screenshot()
            flag = True
        return flag

    #登录成功后可见的元素
    def get_login_success_element(self):
        flag = False
        element = self.find_element("xpath", '//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[2]')
        log.info("element = %s" %element)
        if element !=None:
            self.get_screenshot()
            flag = True
        return flag

    #获取excel数据
    def get_excel_data(self):
        excel_data = GetExcelData()
        data = excel_data.get_all_row_data()
        return data

if __name__ == '__main__':
    lp=LoginPage()
    for i in range(3):
        if i==1:
            driver = lp.open_login_page()
        elif i==2:
            driver = lp.open_login_page("ie")
        else:
            driver = lp.open_login_page("firefox")
    lp.login("","1234567")
    sleep(2)
    lp.get_input_usr_tips()
    sleep(5)
    lp.close_broswer()