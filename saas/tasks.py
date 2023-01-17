from __future__ import absolute_import,unicode_literals
from celery import shared_task
import time
import logging
from saas.saas_program import run_web
import os
from saas.saas_program.common import configDingDing,configHttp
@shared_task
def add(x,y):
    # print("执行celery")
    time.sleep(20)
    print('add执行完毕')
    # return x+y

@shared_task
def runallcase():
    # self.request.__dict__
    # print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time())))
    # configDingDing.sendDingDing({"tests": 1, "passs": 2,
    #                              "failures": 3,
    #                              "errors": 4, "time":time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))})
    # # return '执行celery'



    discover_list = []
    for case in os.listdir(r'./saas/saas_program/testCase'):
        if case.startswith("test"):
            case_path=os.path.join(r'./saas/saas_program/testCase',case)
            discover_list.append(case_path)
    configHttp.Http.host = None
    configHttp.Http.header = None
    run_web.runallcases(discover_list)



@shared_task
def runallcases_by_one_thread():
    discover_list = []
    for case in os.listdir(r'./saas/saas_program/testCase'):
        if case.startswith("test"):
            case_path = os.path.join(r'./saas/saas_program/testCase', case)
            discover_list.append(case_path)
    configHttp.Http.host = None
    configHttp.Http.header = None
    run_web.runallcases_by_one_thread(discover_list)
