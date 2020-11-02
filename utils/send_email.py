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
from utils.get_config_data import GetConfigData
# import utils.global_para as glo

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

    #获取count
    def get_count(self,option):
        filename = os.path.join(get_project_dir(), "ConfigFile", "data.ini")
        cf = GetConfigData(filename)
        data = cf.get_data("count",option)
        return data

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

        # ie = glo.get_value("ie")
        # chrome = glo.get_value("chrome")
        # ff = glo.get_value("firefox")
        # log.info("ie=%s,chrome=%s,ff=%s"%(ie,chrome,ff))
        # broswer=[]
        # if ie != None:
        #     broswer.append("ie")
        #     success_count = glo.get_value("ie_success_count")
        #     failure_count = glo.get_value("ie_failure_count")
        # elif chrome != None:
        #     broswer.append("chrome")
        #     success_count = glo.get_value("ch_success_count")
        #     failure_count = glo.get_value("ch_failure_count")
        # elif ff != None:
        #     broswer.append("firefox")
        #     success_count = glo.get_value("ff_success_count")
        #     failure_count = glo.get_value("ff_failure_count")
        # # total_case_count =
        #邮件正文内容
        # context = "共测试%s个浏览器(%s)。每个浏览器测试%s个用例，其中成功%s个，失败%s个"%(file_num,broswer,(success_count + failure_count),success_count,failure_count)

        # file_2 = os.walk(mail_dir)[2]
        # log.info("file_2=%s" % file_2)
        broswer_type =[]
        for root, dirs, file in os.walk(mail_dir):
            #构造附件
            log.info("file=%s"%file)

            for mail_file in file:
                log.info("mail_file=%s" % mail_file)
                bt = mail_file.split("(")[1].split(")")[0]
                broswer_type.append(bt)
                log.info("broswer_type=%s"%(broswer_type))
                mail_path = os.path.join(mail_dir, mail_file)

                if os.path.isfile(mail_path):
                    att = MIMEText(open(mail_path,"rb").read(),"base64","utf-8")
                    send_file_name = mail_file
                    log.info("send_file_name=%s"%send_file_name)
                    att["Content-Type"] = 'application/octet-stream'
                    att["Content-Disposition"] = 'attachment; filename="%s"'%send_file_name
                    message.attach(att)

        context_start = "共测试%s个浏览器("%(len(broswer_type))
        context_end = "\n具体测试结果见附件。"

        if len(broswer_type)==1:
            context1 = ")。\n%s：共执行-个用例。成功%s个，失败%s个，错误%s个"%(broswer_type[0],self.get_count(broswer_type[0] + "_success_count"),
                                                            self.get_count(broswer_type[0] + "_failure_count"),self.get_count(broswer_type[0] + "_error_count"))
            context = context_start + broswer_type[0] + context1 + context_end

        elif len(broswer_type)==2:
            context1 = ")。\n%s：共执行-个用例。成功%s个，失败%s个，错误%s个。" % (
            broswer_type[0], self.get_count(broswer_type[0] + "_success_count"),
            self.get_count(broswer_type[0] + "_failure_count"), self.get_count(broswer_type[0] + "_error_count"))
            context2 = "\n%s：共执行-个用例。成功%s个，失败%s个，错误%s个" % (
            broswer_type[1], self.get_count(broswer_type[1] + "_success_count"),
            self.get_count(broswer_type[1] + "_failure_count"), self.get_count(broswer_type[1] + "_error_count"))
            context = context_start + broswer_type[0]+","+broswer_type[1] +context1 + context2+ context_end
        elif len(broswer_type)==3:
            context1 = ")。\n%s：共执行-个用例。成功%s个，失败%s个，错误%s个。" % (
                broswer_type[0], self.get_count(broswer_type[0] + "_success_count"),
                self.get_count(broswer_type[0] + "_failure_count"), self.get_count(broswer_type[0] + "_error_count"))
            context2 = "\n%s：共执行-个用例。成功%s个，失败%s个，错误%s个" % (
                broswer_type[1], self.get_count(broswer_type[1] + "_success_count"),
                self.get_count(broswer_type[1] + "_failure_count"), self.get_count(broswer_type[1] + "_error_count"))
            context3 = "\n%s：共执行-个用例。成功%s个，失败%s个，错误%s个" % (
                broswer_type[2], self.get_count(broswer_type[2] + "_success_count"),
                self.get_count(broswer_type[2] + "_failure_count"), self.get_count(broswer_type[2] + "_error_count"))
            context = context_start + broswer_type[0] + "," + broswer_type[1]+"," + broswer_type[2] + context1 + context2 +context3 + context_end
        else:
            log.info("浏览器个数错误")
        message.attach(MIMEText(context))

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