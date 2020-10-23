#coding=utf-8
import psycopg2
from utils.get_config_data import GetConfigData
from BasePage.BasePage import log

class GetDBData:
    def __init__(self):
        #获取数据库配置
        self.get_db_config()
        #连接数据库
        self.con = psycopg2.connect(database=self.db_name, user=self.db_usr, password=self.db_psw, host=self.db_host, port=self.db_port)
        #获取游标
        self.cur = self.con.cursor()

    # 获取数据库配置
    def get_db_config(self):
        cf = GetConfigData()
        self.db_name = cf.get_data("database","db_name")
        self.db_host = cf.get_data("database","db_host")
        self.db_port = cf.get_data("database", "db_port")
        self.db_usr = cf.get_data("database", "db_usr")
        self.db_psw = cf.get_data("database", "db_psw")

    #数据库查询
    def select_db(self,sql):
        #执行sql
        self.cur.execute(sql)
        #获取数据
        data = self.cur.fetchall()
        log.info("data=%s"%data)
        return data

    def close_db(self):
        self.cur.close()
        self.con.close()

if __name__ == '__main__':
    db = GetDBData()
    db.select_db("select count(*) from b_bas_company;")
    db.close_db()


