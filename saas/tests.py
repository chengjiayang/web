import json
import os
import time

import django
from saas.saas_program.common.comdb import db
if __name__ == '__main__':

 os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myweb.settings")
# 导入Django，并启动Django项目

django.setup()

# 然后就可以直接通过此py文件进行调试了
from saas import models
# relations_front = models.relationship.objects.filter(status=True,basecase_id=6,type=0)
# relation_front=relations_front[0]
# dealtype=relation_front.get_dealtype_display()
# x=relation_front.interfaceProcess
# # print(a)
#
# if 'mongodb' in dealtype:
#
#  m_type=relation_front.get_m_type_display()
#  m_table = relation_front.m_table
#  m_query=relation_front.m_query
#  m_order=relation_front.m_order
#  m_result = relation_front.m_result
#  print(m_type,m_table,m_query,m_order,m_result)
# elif '接口' in dealtype:
#  interfaceProcess=relation_front.interfaceProcess
#  print(interfaceProcess)
# elif  'sql' in dealtype:
#  sqls=relation_front.sqls
#  print(sqls)


# **

# db = db('localhost','root','12345678','mywebnew')
# print({'namenew': list({}.values())})
# value='update'
# if value.lower().startswith(('select','update','insert','delete')) :
#  print(True)

# import re
#
# VALUE={"id|solutionId":{"method":"select","table":"user_exam_task","condition":{"latest._id":"$.data",'id':"$.id"},"order":None,"result":{"latest._id":"solutionId","_id":"id"}}}
# value=json.dumps(VALUE)
# pattern=u'\$.[a-zA-Z]+'
# i='x'
# while  re.search(pattern,value):
#
#  value=re.sub(pattern,i,value,1)
#  i=i+'y'
#
# # print(value)
# result_return={'a':1,'b':2}
# print(result_return=={'b':2,'a':1})
#
# # result_return = dict(result_return, **{'': None})
# # print(result_return)
# f='saas/saas_program/testFile/e520c512b87f3945f122b4f78396db44.jpeg'
# print(f.split("saas/saas_program/testFile/")[1])

# x={'mongodb_type': 'select', 'mongodb_table': 'user_exam_task', 'mongodb_query': None, 'mongodb_order': '{"createTime":-1}', 'mongodb_result': '{"_id":"id"}'}



# import re
# pattern = u'\$.[a-zA-Z_]+'
# value_interface = re.search(pattern, json.dumps({'_id': '$.data','name':$})).group()
# # print(value_interface)
#
# import jsonpath
# print(str(jsonpath.jsonpath({'errCode': 0, 'message': '', 'data': '1483007372481712128'}, "$.data")))

# print(type(None))

# result_except={'mongodb_type': 'select', 'mongodb_table': 'user_exam_task', 'mongodb_query': {}, 'mongodb_order': {'createTime': -1}, 'mongodb_result': {'_id': 'id'}}
# db = db('localhost','root','12345678','mywebnew')
# x=db.mongoDB_excute(result_except["mongodb_table"],result_except["mongodb_type"],result_except["mongodb_query"], result_except["mongodb_result"],sorts=result_except["mongodb_order"])
# print(x)


# print( ["mongodb_type", "mongodb_table", "mongodb_query",
#                                                                        "mongodb_order",
#                                                                        "mongodb_result"] in ["mongodb_type", "mongodb_table", "mongodb_query",
#                                                                        "mongodb_order",
#                                                                        "mongodb_result"])

# from  saas import models
# from django.db.models import Max
# id=models.casenew.objects.all().aggregate(Max('id'))["id__max"]+1
# print(id)
# relations=models.relationship.objects.filter(basecase_id=case.id)
# case.id=None
# case.save()
# for relation in relations:
#     relation.id=None
#     relation.basecase_id=case.id
#     relation.save()




import jsonpath
a={"errCode":0,"message":"","data":{"content":[{"id":"1485501752640012288","name":"test123","phone":"13500001111","avatar":"https://v8.51cto.com/test/template/avatar.jpg","jobNumber":"","enabled":True,"deptName":"王者荣耀","positionName":"","teamName":"","createTime":"2022-01-24","type":"BASIC","admin":False,"timeLimit":"0","rights":["BASIC"]},{"id":"1475774845367226368","name":"何九---1","phone":"18300000004","avatar":"https://v8.51cto.com/test/template/avatar.jpg","jobNumber":"","enabled":True,"deptName":"王者荣耀","positionName":"","teamName":"","createTime":"2021-12-28","type":"SENIOR","admin":False,"timeLimit":"0","rights":["HIGHEST"]},{"id":"1475773208858857472","name":"name","phone":"18300000003","avatar":"https://v8.51cto.com/test/template/avatar.jpg","jobNumber":"","enabled":True,"deptName":"王者荣耀","positionName":"","teamName":"","createTime":"2021-12-28","type":"SENIOR","admin":False,"timeLimit":"0","rights":["HIGHEST"]},{"id":"1475770844923957248","name":"一叶知秋呵呵","phone":"18300000002","avatar":"https://v8.51cto.com/test/template/avatar.jpg","jobNumber":"","enabled":True,"deptName":"王者荣耀","positionName":"","teamName":"","createTime":"2021-12-28","type":"SENIOR","admin":False,"timeLimit":"0","rights":["HIGHEST"]},{"id":"1473117956913262592","name":"钟馗","phone":"15100000130","avatar":"https://v8.51cto.com/test/template/avatar.jpg","jobNumber":"","enabled":True,"deptName":"云梦泽","positionName":"","teamName":"","createTime":"2021-12-21","type":"BASIC","admin":False,"timeLimit":"0","rights":["BASIC"]},{"id":"1470346941040676864","name":"超级兵010","avatar":"https://v8.51cto.com/test/template/avatar.jpg","email":"chaojb010@honor.com","enabled":True,"deptName":"你你你","positionName":"","teamName":"","createTime":"2021-12-13","entryTime":"2020-05-27","type":"BASIC","admin":False,"timeLimit":"0","rights":["BASIC"]},{"id":"1470330235551457280","name":"超级兵009","avatar":"https://v8.51cto.com/test/template/avatar.jpg","email":"chaojb009@honor.com","enabled":True,"deptName":"你你你","positionName":"","teamName":"","createTime":"2021-12-13","entryTime":"2020-05-26","type":"BASIC","admin":False,"timeLimit":"0","rights":["BASIC"]},{"id":"1470329822374764544","name":"超级兵008","avatar":"https://v8.51cto.com/test/template/avatar.jpg","email":"chaojb008@honor.com","enabled":True,"deptName":"你你你","positionName":"","teamName":"","createTime":"2021-12-13","entryTime":"2020-05-25","type":"SENIOR","admin":False,"timeLimit":"0","rights":["HIGHEST"]},{"id":"1470324275466436608","name":"超级兵007","avatar":"https://v8.51cto.com/test/template/avatar.jpg","email":"chaojb007@honor.com","enabled":True,"deptName":"你你你","positionName":"","teamName":"","createTime":"2021-12-13","entryTime":"2020-05-24","type":"SENIOR","admin":False,"timeLimit":"0","rights":["HIGHEST"]},{"id":"1468494103305969664","name":"小兵j0966","avatar":"https://v8.51cto.com/test/template/avatar.jpg","email":"binj966@honor.com","enabled":True,"deptName":"小兵分部五","positionName":"中路","teamName":"","createTime":"2021-12-08","entryTime":"2020-05-31","type":"SENIOR","admin":False,"timeLimit":"0","rights":["HIGHEST"]},{"id":"1468494103284998144","name":"小兵j0965","avatar":"https://v8.51cto.com/test/template/avatar.jpg","email":"binj965@honor.com","enabled":True,"deptName":"小兵分部五","positionName":"中路","teamName":"","createTime":"2021-12-08","entryTime":"2020-05-31","type":"SENIOR","admin":False,"timeLimit":"0","rights":["HIGHEST"]},{"id":"1468494103268220928","name":"小兵j0964","avatar":"https://v8.51cto.com/test/template/avatar.jpg","email":"binj964@honor.com","enabled":True,"deptName":"小兵分部五","positionName":"中路","teamName":"","createTime":"2021-12-08","entryTime":"2020-05-31","type":"BASIC","admin":False,"timeLimit":"0","rights":["BASIC"]},{"id":"1468494103230472192","name":"小兵j0963","avatar":"https://v8.51cto.com/test/template/avatar.jpg","email":"binj963@honor.com","enabled":True,"deptName":"小兵分部五","positionName":"中路","teamName":"","createTime":"2021-12-08","entryTime":"2020-05-31","type":"BASIC","admin":False,"timeLimit":"0","rights":["BASIC"]},{"id":"1468403992966905856","name":"ewrrgerrg","phone":"13621871123","avatar":"https://v8.51cto.com/test/template/avatar.jpg","jobNumber":"","enabled":True,"deptName":"稷下学院","positionName":"","teamName":"","createTime":"2021-12-08","type":"BASIC","admin":False,"timeLimit":"0","rights":["BASIC"]},{"id":"1468179062518104064","name":"曜","phone":"15100000123","avatar":"https://v8.51cto.com/test/template/avatar.jpg","jobNumber":"","email":"123qw@qq.com","enabled":True,"deptName":"云梦泽","positionName":"","teamName":"","createTime":"2021-12-07","type":"BASIC","admin":False,"timeLimit":"0","rights":["BASIC"]},{"id":"1468136707391926272","name":"小兵1000","avatar":"https://v8.51cto.com/test/template/avatar.jpg","email":"bing1000@honor.com","enabled":True,"deptName":"小兵分部五","positionName":"下路","teamName":"","createTime":"2021-12-07","entryTime":"2020-05-31","type":"SENIOR","admin":False,"timeLimit":"0","rights":["HIGHEST"]},{"id":"1468136707375149056","name":"小兵0999","avatar":"https://v8.51cto.com/test/template/avatar.jpg","email":"bing999@honor.com","enabled":True,"deptName":"小兵分部五","positionName":"下路","teamName":"","createTime":"2021-12-07","entryTime":"2020-05-31","type":"SENIOR","admin":False,"timeLimit":"0","rights":["HIGHEST"]},{"id":"1468136707337400320","name":"小兵0998","avatar":"https://v8.51cto.com/test/template/avatar.jpg","email":"bing998@honor.com","enabled":True,"deptName":"小兵分部五","positionName":"下路","teamName":"","createTime":"2021-12-07","entryTime":"2020-05-31","type":"SENIOR","admin":False,"timeLimit":"0","rights":["HIGHEST"]},{"id":"1468136707316428800","name":"小兵0997","avatar":"https://v8.51cto.com/test/template/avatar.jpg","email":"bing997@honor.com","enabled":True,"deptName":"小兵分部五","positionName":"下路","teamName":"","createTime":"2021-12-07","entryTime":"2020-05-31","type":"SENIOR","admin":False,"timeLimit":"0","rights":["HIGHEST"]},{"id":"1468136707303845888","name":"小兵0996","avatar":"https://v8.51cto.com/test/template/avatar.jpg","email":"bing996@honor.com","enabled":True,"deptName":"小兵分部五","positionName":"下路","teamName":"","createTime":"2021-12-07","entryTime":"2020-05-31","type":"SENIOR","admin":False,"timeLimit":"0","rights":["HIGHEST"]}],"total":"37052"}}
# print(jsonpath.jsonpath(a, '$.data.content[-1:].id')[0])

# from django.forms.models import model_to_dict
# def lgetCasebyId(tablename, id):
#  case_result = tablename.objects.get(id=id)
#  # relates=relationship.objects.filter(status=True,basecase_id=id)
#  try:
#   file = case_result.file.url
#  except:
#   file = None
#  case = model_to_dict(case_result)
#  case.pop("related")
#  case["method"] = case_result.get_method_display()
#  case["file"] = file
#  case['name']=str(case['id'])
#  return case
#
#
# print(lgetCasebyId(models.casenew,14))


import logging
from saas.saas_program import readConfig
import unittest
from saas.saas_program.common import xlsxRead, configHttp, runCase1102, com, cominterface1202, mywebDB
from io import StringIO

from ddt import data, ddt

logging.basicConfig(level=logging.INFO)


# len=list(range(0,3))
# @ddt
# from saas.saas_program.common import configHttp
# from saas.saas_program import readConfig
# def login():
#  datas = mywebDB.getCasebyId(models.casenew, 2)
#  url = datas["url"]
#  # self.logger.debug(url)
#  method = datas["method"]
#  params = datas["url_params"]
#  data = readConfig.get_user()
#  # data=mywebDB.getCasebyId()
#  header = readConfig.get_header()
#  http = configHttp.Http().execute(url, method, params, data)
#
#
#  return http.json()
#
#
#
#
# print(login())
#



# datas = {"username": '1', "password": '2', "type": "password"}
# datas=str(datas)
# print(datas)
# print(type(datas))
#
# project_result = models.configs.objects.get(platform=0, status=True)
# datas = {"username": project_result.account, "password": project_result.password, "type": "password"}
# print(datas)
# import time
# print()
# # print('test_%s.py' % ('1'+str(time.time())))
# get_is_online={True: '支持', False: '不支持'}
# obj = models.casenew.objects.get(id=30)
# # obj.is_online = get_is_online[obj.is_online]
# print(obj.is_online)

# import saas.saas_program.common.mywebDB
# case = mywebDB.lgetCasebyId(models.casenew, 29)
# print(case["is_online"])


# x={'a':1}
# if not x.get('a'):
#  print('ok')

# class A():
#  value=None
#  # def __new__(cls, v,x):
#  #  if not hasattr(cls, "_instance"):
#  #   cls._instance = super().__new__(cls)
#  #  return cls._instance
#
#  def __init__(self,v,x):
#   if not A.value:
#    A.value=v
#   self.x=x
#
# x=A(1,0)
# # print(x.x)
# # x.value=0
# y=A(2,1)
# print(y.x)
# print(x.x)

import logging
from saas.saas_program import readConfig
import unittest
from saas.saas_program.common import xlsxRead, configHttp, runCase1102, com, cominterface1202, mywebDB
from io import StringIO

from ddt import data, ddt

logging.basicConfig(level=logging.INFO)
import threading


# len=list(range(0,3))
# @ddt


import jsonpath
x={"errCode":0,"message":"","data":{"content":[{"id":"1496013434835210240","examId":"1496013434700992512","title":"问答题1","thumbnail":"https://v8.51cto.com/template/exam/cover/cover1.jpg","startTime":"2021-07-23 10:00:00","endTime":"2022-02-22 15:06:00","duration":0,"count":"1","score":0,"submitCount":0,"passed":False,"passScore":0,"retryCount":-1,"scoring":0,"hidePassed":False,"hideScore":False,"device":"BOTH","expired":True},{"id":"1496013436781367296","examId":"1496013436731035648","title":"问答题1","thumbnail":"https://v8.51cto.com/template/exam/cover/cover1.jpg","startTime":"2021-07-23 10:00:00","endTime":"2022-02-22 15:06:00","duration":0,"count":"1","score":0,"submitCount":0,"passed":False,"passScore":0,"retryCount":-1,"scoring":0,"hidePassed":False,"hideScore":False,"device":"BOTH","expired":True},{"id":"1496013452992352256","examId":"1496013452937826304","title":"问答题1","thumbnail":"https://v8.51cto.com/template/exam/cover/cover1.jpg","startTime":"2021-07-23 10:00:00","endTime":"2022-02-22 15:06:00","duration":0,"count":"1","score":0,"submitCount":0,"passed":False,"passScore":0,"retryCount":-1,"scoring":0,"hidePassed":False,"hideScore":False,"device":"BOTH","expired":True},{"id":"1496013724116357120","examId":"1496013723982139392","title":"问答题1","thumbnail":"https://v8.51cto.com/template/exam/cover/cover1.jpg","startTime":"2021-07-23 10:00:00","endTime":"2022-02-22 15:07:00","duration":0,"count":"1","score":0,"submitCount":0,"passed":False,"passScore":0,"retryCount":-1,"scoring":0,"hidePassed":False,"hideScore":False,"device":"BOTH","expired":True},{"id":"1499358070861508608","examId":"1499358070794399744","title":"问答题2022-03-031","thumbnail":"https://v8.51cto.com/template/exam/cover/cover1.jpg","startTime":"2022-03-03 10:00:00","endTime":"2022-03-03 20:36:00","duration":0,"count":"1","score":0,"submitCount":0,"passed":False,"passScore":0,"retryCount":-1,"scoring":0,"hidePassed":False,"hideScore":False,"device":"BOTH","expired":False},{"id":"1499358072614727680","examId":"1499358072576978944","title":"问答题2022-03-031","thumbnail":"https://v8.51cto.com/template/exam/cover/cover1.jpg","startTime":"2022-03-03 10:00:00","endTime":"2022-03-03 20:36:00","duration":0,"count":"1","score":0,"submitCount":0,"passed":False,"passScore":0,"retryCount":-1,"scoring":0,"hidePassed":False,"hideScore":False,"device":"BOTH","expired":False}],"total":"6"}}

a=''
print(jsonpath.jsonpath(x,a))

from saas.tasks import add, runallcase,runallcases_by_one_thread
from celery.app.control import  Control
from myweb.celery import  app
from celery.result import AsyncResult

# result=runallcase.delay()
# print('开始执行')
# # print(type(result.id))
# celery_control=Control(app=app)
# celery_control.cancel_consumer()
 # .revoke()

# a={}
# a['a']=0
# print(a)
res={'a':1,'x':0}.pop('a')
print(res)