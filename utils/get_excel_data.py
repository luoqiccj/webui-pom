#coding=utf-8
import xlrd
import xlwt
from xlutils.copy import copy
from utils.get_info import log
import os

class GetExcelData:
    def __init__(self):
        pass

    # 获取当前项目工作目录
    def get_pj_dir(self):
        pj_dir = os.path.abspath(os.path.dirname(os.getcwd()))
        log.info("pj_dir = %s" % pj_dir)
        return pj_dir

    #打开excel文件指定工作簿
    def open_excel_file(self,excel_file=None):
        if excel_file==None:
            pj_dir = self.get_pj_dir()
            excel_file = os.path.join(pj_dir,"ExcelFile","login_test.xls")
        self.excel_file_name = excel_file
        self.rd = xlrd.open_workbook(excel_file)
        self.sheet = self.rd.sheet_by_index(0)

    #获取行数
    def get_row_count(self):
        nrows = self.sheet.nrows
        log.info("nrows=%s"%nrows)
        return nrows

    #获取单元格数据
    def get_cell_value(self,row,col):
        data = self.sheet.cell(row,col)
        return data

    #获取指定行数据
    def get_row_value(self,row):
        data = self.sheet.row_values(row)
        return data

    # 获取指定列数据
    def get_col_value(self, col):
        data = self.sheet.col_values(col)
        return data

    #获取所有行数据
    def get_all_row_data(self):
        nrows = self.get_row_count()
        log.info("nrows=%s" % nrows)
        data = []
        for row in range(1,nrows):
            row_data = self.get_row_value(row)
            data.append(row_data)
        log.info("data=%s"%data)
        return data

    #指定单元格写入数据
    def write_data(self,row,col,value):
        old_excel = self.rd
        new_excel = copy(old_excel)
        sheet = new_excel.get_sheet(0)
        sheet.write(row,col,value)
        new_excel.save(self.excel_file_name)

if __name__ == '__main__':
    ed = GetExcelData()
    ed.open_excel_file()
    ed.get_row_count()
    data = ed.get_cell_value(1,1)
    log.info("data=%s"%(data))
    log.info("get_row_value=%s"%(ed.get_row_value(1)))
    log.info("get_col_value=%s" % (ed.get_col_value(1)))
    ed.write_data(1,3,"write test")
    ed.get_all_row_data()