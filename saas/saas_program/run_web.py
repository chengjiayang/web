# 1.setupclass里设置self.xxx变量，不同用例之间无法实时共享参数变动
# from settings import *
import requests,json
import unittest

#
# class Login(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(self):
#         api_token = '/v1/api/common/getToken'
#         # self.real_token_url = API_TEST_BASE_URL + api_token
#         self.token = 12345
#     def test_get_token(self):
#         # r = requests.post(url=self.real_token_url)
#         self.token = 678
#         print("第一个case获得的token：",self.token)
#         return self.token
#
#     def test_get_u(self):
#         print("第二个case获得token值：",self.token)
#
#
# if __name__ == '__main__':
#     unittest.main()
#
# discover = unittest.defaultTestLoader.discover(r'C:\Users\51cto\Desktop\hm_api-master-4b3abf9d035e86f5c28e76ae5294e4bde74cad4f\hm_api-master-4b3abf9d035e86f5c28e76ae5294e4bde74cad4f\hm\testCase', pattern="test*.py", top_level_dir=None)
# print(discover)
import  HTMLTestRunner
import  os
import time
from saas.saas_program import HTMLTestRunnerCN
# from concurrent.futures import  ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
# from Threadpool
import logging
# logging.disable(logging.INFO)
import re
from saas.saas_program.common import  comReport,creatCaseFile1102,configEmail,configDingDing
from saas.saas_program import readConfig
import datetime

import threading
def get_logName(filename):
    b = filename[5:-3]
    return b


def get_cases_discover():
    discover_list=[]
    for case in os.listdir(r'./saas/saas_program/testCase'):
        if case.startswith("test"):
            discover = unittest.defaultTestLoader.discover(r'./saas/saas_program/testCase', pattern=f"{case}", top_level_dir=None)
            case_one={"name":case,"discover":discover}
            discover_list.append(case_one)


    return discover_list


# get_case_discover()
def runcase(case):
    # print("%s开始时间:%s" % (case["name"],time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))))
    report_abspath = os.path.join(r'./saas/saas_program/testFile', "result_" + case["name"] + ".html")
    fp = open(report_abspath, "wb")
    logger = logging.getLogger(get_logName(case["name"]))
    runner = HTMLTestRunnerCN.HTMLTestReportCN(stream=fp,
                                           # verbosity=2,
                                           title=u'saas接口自动化测试报告',
                                           description=u'用例执行情况：',
                                           custom_logger=logger
                                           )
    # # 4、调用add_case函数返回值
    result = runner.run(case["discover"])
    # print("%s结束时间:%s" % (case["name"], time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))))


# def createcasefile(caseslist):
#     files=[]
#     for case in caseslist:
#         files.append(creatCaseFile1102.create(case))
#     return files

#多线程执行
def runallcases(files=None):
    print("多线程")
    start_time = datetime.datetime.now()
    cases_discover = get_cases_discover()

    pool = ThreadPoolExecutor(max_workers=30)

    all_task = [pool.submit(runcase, case_one) for case_one in cases_discover]
    wait(all_task, return_when=ALL_COMPLETED)

    end_time = datetime.datetime.now()
    comReports = comReport.Report()
    comReport.Report.datas = comReports.datas_processing()
    comReports.merge_reports(start_time, end_time - start_time)
    comReports.create_report_email(start_time, end_time - start_time)
    print('测试时长：%s' % (end_time - start_time))

    # 删除测试用例文件
    for file in files:
        os.remove(file)

    # configEmail.sendEmail()
    #
    # configDingDing.sendDingDing({"tests": comReport.Report.datas[1], "passs": comReport.Report.datas[2],
    #                              "failures": comReport.Report.datas[3],
    #                              "errors": comReport.Report.datas[4], "time": (end_time - start_time)})



#单线程执行
def runallcases_by_one_thread(discover_list):

    print("单线程")



    fp_log = open(r'./templates/Result_log.html', "wb")
    runner_log = HTMLTestRunnerCN.HTMLTestReportCN(stream=fp_log,

                                                   title=u'saas接口自动化测试报告',
                                                   description=u'用例执行情况：',
                                                   custom_logger=logging.getLogger()
                                                    )
    discover = unittest.defaultTestLoader.discover(r'./saas/saas_program/testCase', pattern="test*.py", top_level_dir=None)
    result_log = runner_log.run(discover)
    fp_log.close()

    counts = result_log.success_count + result_log.failure_count + result_log.error_count
    configDingDing.sendDingDing(
        {"tests": counts, "passs": result_log.success_count, "failures": result_log.failure_count,
         "errors": result_log.error_count,"time":1})

    for file in discover_list:
       os.remove(file)








