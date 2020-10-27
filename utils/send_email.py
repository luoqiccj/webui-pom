#coding=utf-8
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from utils.get_config_data import GetConfigData
from utils.get_info import log
from  utils.get_info import get_project_dir
from  utils.get_info import get_cur_date
import glob

class SendMail:
    def __init__(self):
        pass

    def send_mail(self,report_name,success_case_count,failure_case_count):
        #获取mail的配置信息
        self.get_mail_config()
        #创建一个带附件的实例
        message = MIMEMultipart()
        subject = " WEBUI自动化测试结果"
        message['Subject']=subject
        message['from']=self.from_addr
        message['to'] = self.to_addrs

        #邮件正文内容
        total_case_count = success_case_count + failure_case_count
        context = "共测试%d个用例，成功%d个，失败%d个。\n具体测试结果见附件。"%(total_case_count,success_case_count,failure_case_count)
        message.attach(MIMEText(context))

        #构造附件1
        att1 = MIMEText(open(report_name,"rb").read(),"base64","utf-8")
        send_file_name = report_name.split("/")[-1]
        log.info("send_file_name=%s"%send_file_name)
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="%s"'%send_file_name
        message.attach(att1)

        try:
            self.st = smtplib.SMTP()
            self.st.connect(host=self.mail_host)
            log.info("self.mail_usr=%s,self.mail_psw=%s"%(self.mail_usr,self.mail_psw))
            self.st.login(self.mail_usr,self.mail_psw)
            self.st.sendmail(self.from_addr,self.to_addrs.split(";"), message.as_string())
            log.info("send email success")
        except:
            log.info("send email fail")

    # 获取mail的配置信息
    def get_mail_config(self):
        cf = GetConfigData()
        self.mail_host = cf.get_data("mail","mail_host")
        self.mail_port = cf.get_data("mail", "mail_port")
        self.mail_usr = cf.get_data("mail", "mail_usr")
        self.mail_psw = cf.get_data("mail", "mail_psw")
        self.from_addr = cf.get_data("mail", "from_addr")
        self.to_addrs = cf.get_data("mail", "to_addrs")

    def send_mail_dir(self,mail_dir):
        #获取mail的配置信息
        self.get_mail_config()
        #创建一个带附件的实例
        message = MIMEMultipart()
        subject = " WEBUI自动化测试结果"
        message['Subject']=subject
        message['from']=self.from_addr
        message['to'] = self.to_addrs

        file_num = len(glob.glob(mail_dir+"\\"+"*.html"))
        log.info("file_num=%s"%(file_num))

        #邮件正文内容
        context = "共测试%s个浏览器"%file_num
        message.attach(MIMEText(context))

        # file_2 = os.walk(mail_dir)[2]
        # log.info("file_2=%s" % file_2)
        for root, dirs, file in os.walk(mail_dir):
            #构造附件
            log.info("file=%s"%file)
            for mail_file in file:
                log.info("mail_file=%s" % mail_file)
                mail_path = os.path.join(mail_dir, mail_file)
                if os.path.isfile(mail_path):
                    att = MIMEText(open(mail_path,"rb").read(),"base64","utf-8")
                    send_file_name = mail_file
                    log.info("send_file_name=%s"%send_file_name)
                    att["Content-Type"] = 'application/octet-stream'
                    att["Content-Disposition"] = 'attachment; filename="%s"'%send_file_name
                    message.attach(att)

        try:
            self.st = smtplib.SMTP()
            self.st.connect(host=self.mail_host)
            log.info("self.mail_usr=%s,self.mail_psw=%s"%(self.mail_usr,self.mail_psw))
            self.st.login(self.mail_usr,self.mail_psw)
            self.st.sendmail(self.from_addr,self.to_addrs.split(";"), message.as_string())
            log.info("send email success")
        except:
            log.info("send email fail")

    #关闭连接
    def close_mail(self):
        self.st.close()

if __name__ == '__main__':
    sm=SendMail()
    pj_dir = get_project_dir()
    cur_date = get_cur_date()
    mail_dir = os.path.join(pj_dir,"Report",cur_date)
    log.info("mail_dir=%s"%mail_dir)
    sm.send_mail_dir(mail_dir)
    sm.close_mail()