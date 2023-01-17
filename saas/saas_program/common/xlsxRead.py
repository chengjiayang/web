import os
import sys
curPath =os.path.abspath(os.path.abspath(__file__))
rootPath=os.path.split(curPath)[0]
sys.path.append(curPath)
# print(sys.path)
import json
import logging
logging.basicConfig(level=logging.INFO)
#logging.disable(logging.INFO)


# import openpyxl
import xlrd
# sys.path.append("")
class casesRead():
    allCases = None
    front_login_case = None
    backend_login_case = None
    def __init__(self,xlsxfile,sheetname):
        self.xlsxfile=xlsxfile
        self.sheetname=sheetname
        # self.Allcase=self.readxlsx() #看能不能用这个优化

    def readxlsx(self):
        # tests = openpyxl.load_workbook(self.xlsxfile)
        tests=xlrd.open_workbook(self.xlsxfile)
        # sheett = tests[self.sheetname]
        sheett=tests.sheet_by_name(self.sheetname)
        # rown = sheett.max_row
        rown=sheett.nrows
        # coln = sheett.max_column
        coln=sheett.ncols
        datasdict = {}
        for rowi in range(1, rown):
            datalistsingle = []
            for coli in range(0, coln):
                data = sheett.cell(rowi, coli).value
                datalistsingle.append(data)
            logging.debug(datalistsingle)
            datasdict.setdefault(rowi, datalistsingle)

        return datasdict

    def get_cases(self):
        return list(self.readxlsx().values())

    def get_one_case(self,rown):
        return self.readxlsxNew()[rown]

    def get_one_caseNews(self,rown):
        '''需提前调用setAllcases'''
        return casesRead.allCases[rown]

    def get_name(self,case):
        return case[0]
    def get_url(self,case):
        return case[1]
    def get_method(self,case):
        return case[2]
    def get_url_params(self,case):
        return case[3]
    def get_body_params(self,case):
        return case[4]
    def get_expectedResult(self,case):
        expectedResult={}
        expectedResult['code']=case[7]
        expectedResult["unchange"]=case[8]
        expectedResult["change"] = case[9]
        return expectedResult

    # def get_apichinese(self,case):



    def readxlsxNew(self):
        '''返回case集合list,case格式为dict'''
        # tests = openpyxl.load_workbook(self.xlsxfile)
        tests = xlrd.open_workbook(self.xlsxfile)
        # sheett = tests[self.sheetname]
        sheett=tests.sheet_by_name(self.sheetname)
        rown = sheett.nrows
        logging.debug(rown)
        coln = sheett.ncols
        logging.debug(coln)
        cases = {}
        for rowi in range(1, rown):
            case = {}
            case["rown"]=rowi+1
            case["name"]=sheett.cell(rowi, 0).value
            case["url"] = sheett.cell(rowi, 1).value
            case["method"] = sheett.cell(rowi, 2).value
            case["url_params"] = sheett.cell(rowi, 3).value
            case["body_params"] = sheett.cell(rowi, 4).value
            case["file"]=sheett.cell(rowi, 5).value
            case["frontCase"]=sheett.cell(rowi, 6).value
            case["exceptReponse"] = {"code":sheett.cell(rowi, 7).value,
                                                                    "unchange":sheett.cell(rowi, 8).value,
                                                                    "change":sheett.cell(rowi, 9).value}

            case['chinese']=sheett.cell(rowi, 10).value
            case['lastCase']=sheett.cell(rowi, 11).value
            case['sql']=sheett.cell(rowi, 12).value
            case['lastSql']=sheett.cell(rowi, 13).value
            case['redis'] = sheett.cell(rowi, 14).value
            case['mongoDB'] = sheett.cell(rowi, 15).value
            # logging.info("测试用例参数：")
            # logging.info(case)
            # print(case)

            cases[rowi+1]=case
        # print(cases)
        return cases

    def get_one_caseNew(self,rown):
        return self.readxlsxNew()[rown]

    def get_one_caseByName(self,caseName):
        for case in self.readxlsxNew().values():
            if self.get_nameNew(case)==caseName:
                return case

    def setAllcases(self):
        '''全部用例数据获取'''
        casesRead.allCases=self.readxlsxNew()



    def get_nameNew(self,case):
        return case["name"]
    def get_urlNew(self,case):
        return case["url"]
    def get_methodNew(self,case):
        return case["method"]
    def get_url_paramsNew(self,case):
        return case["url_params"]
    def get_body_paramsNew(self,case):
        return case["body_params"]
    def get_file(self,case):
        return case["file"]
    def get_frontCase(self,case):
        '''获取前置接口及取参信息'''
        return case["frontCase"]
    def get_expectedResultNew(self,case):
        return case["exceptReponse"]

    def get_lastCase(self,case):
        return case["lastCase"]


