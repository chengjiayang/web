import json
import re
import os
import requests
from saas.saas_program import readConfig
import logging
logging.basicConfig(level=logging.INFO)
#logging.disable(logging.INFO)



def sendDingDing(result):
    DingDingUrl=readConfig.get_DingDing_url()
    a = {
        "msgtype": "text",
        "text": {
            "content": "saas接口测试报告："+"%s\n"%readConfig.get_testSheet()
                       + "总用例数：" + str(result["tests"]) + '\n'
                       + "成功数：" +str(result["passs"])+ '\n'
                       + "失败数：" + str(result["failures"]) + '\n'
                       + "错误数：" + str(result["errors"]) + '\n'
                       +"执行时长："+str(result["time"])+ '\n'
                       + '详情可查看邮件'
        }
    }
    a = json.dumps(a)
    # print(type(a))
    # logging.info(a)
    headers = {
        "Content-Type": "application/json"
    }

    requests.request(method='post',
                     url=DingDingUrl,
                     data=a, headers=headers)



# sendDingDing({"tests":"1","passs":"2","failures":"3","skipped":"4"})





