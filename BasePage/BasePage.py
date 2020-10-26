#coding=utf-8
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from utils.get_info import log
from utils.get_info import get_project_dir
from utils.get_info import get_cur_date
import traceback

class BasePage:
    #打开浏览器
    def open_broswer(self,broswer_type=None):
        #未传浏览器类型，默认打开谷歌浏览器
        if broswer_type==None:
            driver = webdriver.Chrome()
        else:
            #打开谷歌浏览器
            if broswer_type=='chrome':
                driver = webdriver.Chrome()
            # 打开火狐浏览器
            elif  broswer_type=='firefox':
                driver = webdriver.Firefox()
            # 打开IE浏览器
            elif  broswer_type=='ie':
                driver = webdriver.Ie()
            else:
            # 参数错误，提示不支持
                log.info("not support broswer type")
        driver.maximize_window()
        self.driver = driver
        return driver
    #打开链接页面
    def open_url(self,driver,url):
        #打开url页面
        driver.get(url)

    #定位元素,传入定位方式、位置
    def find_element(self,by,locator):
        try:
            if by=="id":
                log.info("by=%s,locator=%s"%(by,locator))
                wait = WebDriverWait(self.driver,10,1)
                lt = (By.ID,locator)
                wait.until(ec.visibility_of_element_located(lt))
                element=self.driver.find_element_by_id(locator)
            elif by=="xpath":
                log.info("by=%s,locator=%s"%(by,locator))
                wait = WebDriverWait(self.driver,10,1)
                lt = (By.XPATH,locator)
                wait.until(ec.visibility_of_element_located(lt))
                element=self.driver.find_element_by_xpath(locator)
        except:
            element = None
        return element

    #点击元素
    def click_element(self,by,locator):
        self.find_element(by,locator).click()

    #发送文本
    def send_text(self,by, locator,value):
        self.find_element(by, locator).send_keys(value)

    #关闭浏览器，释放进程
    def close_broswer(self):
        self.driver.quit()

    #截图
    def get_screenshot(self):
        #获取调用该函数的函数名
        func_name = traceback.extract_stack()[-2][2]
        #截图文件路径
        dir = get_project_dir() + "\ScreenShot\\"
        #截图文件命名 调用函数+日期.png
        filename = dir + func_name + "_" + get_cur_date() + ".png"
        log.info("filename=%s" % filename)
        self.driver.save_screenshot(filename)

if __name__ == '__main__':
    bp = BasePage()
    driver = bp.open_broswer()
    bp.open_url(driver,"http://www.baidu.com")
    bp.send_text("id","kw","测试")
    sleep(2)
    element=bp.click_element("id","su")
    sleep(2)
    bp.close_broswer()





