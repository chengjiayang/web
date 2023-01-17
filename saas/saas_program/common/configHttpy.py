import requests
import json
from  saas.saas_program.common  import xlsxRead,com,comdb
import logging
import re
import os
import time
import re
from saas import models
logging.basicConfig(level=logging.INFO)
#logging.disable(self.logger.info)
from  saas.saas_program import readConfig
from requests_toolbelt import MultipartEncoder
from  urllib3 import encode_multipart_formdata
# from datetime import datetime
import datetime
import jsonpath
from saas.saas_program.common import cominterface1102
# from cominterface import interface
from  saas.saas_program.common import mywebDB
class Http():
    def __init__(self,environment,caseName=None):

        readConfig.environment_djangoWeb=environment

        self.host=readConfig.get_host()
        self.header=readConfig.get_header()

        self.logger = logging.getLogger(caseName)
        # self.interface=cominterface.interface(caseName)
        self.log_name=caseName





#  可用且文件上传OK，待调
    def execute(self,url,type,params,data):

        http=requests.request(method=type,url=self.host+url,params=params,data=data,headers=self.header,verify=False)

        return http

    def executef(self, url, type, params, data):
        http = requests.request(method=type, url=self.host + url, params=params, files=data,headers=self.header,verify=False)
        return http



#,headers=self.header


    #saas的登录验证
    def login(self,login_data):
        datas=mywebDB.getCasebyId(models.casenew,2)
        url=datas["url"]
        self.logger.debug(url)
        method=datas["method"]
        params=datas["url_params"]

        if type(login_data)==dict:
            login_data=json.dumps(login_data)
        data=login_data

        self.header=readConfig.get_header()
        # self.logger.info(data)
        # self.logger.info(type(data))
        http=self.execute(url,method,params,data)
        # print(http)
        return http
    #saas的登录验证
    def getauth(self,login_data):
        '''登录并获取验签，并整合到header中'''
        if not self.header.get("Authorization"):
            http = self.login(login_data)

            # self.logger.info("登陆请求路径：%s" % str(http.request.url))
            # self.logger.info("登陆请求参数：%s" % str(http.request.body))
            # self.logger.info("登陆请求方法：%s" % str(http.request.method))
            # self.logger.info("登陆返回码：%s" % str(http.status_code))
            # self.logger.info("登陆返内容：%s" % str(http.json()))

            if http.status_code == 200:
                self.logger.debug('登陆接口返回：{returns}'.format(returns=http.json()))
                if http.json()['errCode'] == 0:
                    self.header["Authorization"] = "bearer {}".format(http.json()['data']["access_token"])
            else:
                self.logger.info("登录失败")
            self.logger.info("登录后header：" + str(self.header))


        return self.header





    def newfile(self,name, text):
        '''下载类接口，保存文件'''
        filepath = os.path.join(os.getcwd(),'testFile/DownloadFiles/%s.xlsx'%name)
        file = open(filepath, 'wb')
        file.write(text)
        file.close()

    # def assertResult(self,http,case ):
    #
    #     '''根据http请求结果与用例预期结果匹配，判断执行结果，并返回（有最基本200返回判断）'''
    #     expectedResult=case["exceptReponse"]
    #     try:
    #         httpReponse=http.json()
    #     except:
    #         # httpReponse=eval(http.text)
    #         httpReponse=None
    #     if expectedResult['code'] !=200:
    #         if http.status_code==expectedResult['code']:
    #             return True
    #         else:
    #             self.logger.info("%s接口返回码与期望值不符"%str(case["name"]))
    #             return False
    #     elif expectedResult['code']==200:
    #         if http.status_code==expectedResult['code']:
    #             if expectedResult["unchange"] != '':
    #                 self.logger.debug("unchange")
    #                 self.logger.debug(expectedResult["unchange"])
    #                 # self.logger.info(type(json.loads(expectedResult["unchange"])))
    #                 # self.logger.info('期望json:')
    #
    #                 if httpReponse == json.loads(expectedResult["unchange"]):
    #                     return True
    #                 else:
    #                     self.logger.info("%s期望返回json:%s" % (case["name"], json.loads(expectedResult["unchange"])))
    #                     self.logger.info("%s接口返回整体与期望不符"% (case["name"]))
    #                     return False
    #             if expectedResult["change"] != '':
    #                 if expectedResult["change"]=='特殊接口：结果非json':
    #                     return True
    #                 elif expectedResult["change"]=='下载类接口':
    #                     self.newfile(case["information"],http.content)
    #                     return True
    #                 else:
    #                     if com.find(expectedResult["change"], httpReponse):
    #                         return True
    #                     else:
    #                        self.logger.info("%s接口返回键值中未包含期望键值:%s"%(str(case["name"]),str(expectedResult["change"])))
    #                        return False
    #         else:
    #             self.logger.info("%s接口返回码与期望值不符"%str(case["name"]))
    #             return False

    def assertResult(self,http,case ):

        '''根据http请求结果与用例预期结果匹配，判断执行结果，并返回（有最基本200返回判断）'''

        try:
            httpReponse=http.json()
        except:
            # httpReponse=eval(http.text)
            httpReponse=None

        if http.status_code==case['code']:
            if (case["unchange"] != '') and  (case["unchange"] != None) :
                self.logger.debug("unchange")
                self.logger.debug(case["unchange"])
                # self.logger.info(type(json.loads(expectedResult["unchange"])))
                # self.logger.info('期望json:')

                if httpReponse == json.loads(case["unchange"]):
                    return True
                else:
                    self.logger.info("%s期望返回json:%s" % (case["name"], json.loads(case["unchange"])))
                    self.logger.info("%s接口返回整体与期望不符" % (case["name"]))
                    return False
            if (case["change"] != '')and  (case["unchange"] != None) :
                if case["change"] == '特殊接口：结果非json':
                    return True
                elif case["change"] == '下载类接口':
                    self.newfile(case["information"], http.content)
                    return True
                else:
                    if com.find(case["change"], httpReponse):
                        value=com.getValue(case["change"], httpReponse)
                        print(type(value))
                        if (value=='') or (value==[]) or (value=='0')   or ((value==0) and (str(value)!='False')):
                            self.logger.info("%s接口返回键值中%s返回空值(空或0):值为%s" % (str(case["name"]), str(case["change"]),str(value)))
                            return False
                        else:
                            return True
                    else:
                        self.logger.info("%s接口返回键值中未包含期望键值:%s" % (str(case["name"]), str(case["change"])))
                        return False
            return True
        else:
            self.logger.info("%s接口返回码与期望值不符" % str(case["name"]))
            self.logger.info('接口返回码{code}，类型{type}'.format(code=http.status_code,type=str(type(http.status_code))))
            self.logger.info('{casename}接口期望返回码{code}，类型{type}'.format(casename=case['name'],code=case['code'], type=str(type(case['code']))))


            return False


    def assertInterfacePass(self,http,case ):

        '''根据http请求结果基本200返回判断'''
        # expectedResult=case["code"]



        if http.status_code==case['code']:

            return True
        else:
            self.logger.info("%s接口返回码与期望值不符"%str(case["name"]))
            self.logger.info('接口返回码{code}，类型{type}'.format(code=http.status_code, type=str(type(http.status_code))))
            self.logger.info('{casename}接口期望返回码{code}，类型{type}'.format(casename=case['name'], code=case['code'],
                                                                       type=str(type(case['code']))))
            return False





    def getResult(self,http,case,result_except):
        '''从http请求结果中取出有用的参数值，组成dict返回'''
        '''待具体情况细化'''
        result_return = {}
        # self.logger.info("执行getResult{http},{case},case类型{type},{result_except}result_except类型{type2}".format(
        #     http=http,case=case,type=str(type(case)),result_except=result_except,type2=str(type(result_except))))


        if self.assertInterfacePass(http, case):


            if type(result_except)==str:
                try:
                    result_except=json.loads(result_except)
                except:
                    self.logger.info("{casename}执行后，数据处理{result_except}非字典格式。所以未处理需要数据".format(casename=case["name"],result_except=result_except))
            if type(result_except)==dict:
                for key, value in result_except.items():

                    if key == 'lastApi':
                        result_return = dict(result_return, **{key: value})
                        continue

                    if (type(value) == str):
                        # 单纯接口取值
                        if value.startswith('$'):
                            value = value
                            try:
                                result_return = dict(result_return, **{key: jsonpath.jsonpath(http.json(), value)[0]})
                            except:
                                result_return = dict(result_return, **{key: None})
                        # 可处理sql中包含接口取值（sql处理第一步）
                        elif (not value.startswith('$')) and ('$' in value):
                            pattern = u'\$.[a-zA-Z_]+'
                            while re.search(pattern, value):
                                value_interface = re.search(pattern, value).group()
                                value = re.sub(pattern, str(jsonpath.jsonpath(http.json(), value_interface)[0]), value,
                                               1)
                    # 可处理mongodb字典中包含的接口取值(mongodb处理第一步)
                    elif (type(value) == dict):
                        try:
                            value = json.dumps(value)
                            if (not value.startswith('$')) and ('$' in value):
                                pattern = u'\$.[a-zA-Z_]+'
                                while re.search(pattern, value):
                                    value_interface = re.search(pattern, value).group()
                                    value = re.sub(pattern, str(jsonpath.jsonpath(http.json(), value_interface)[0]),
                                                   value,
                                                   1)
                                try:
                                    value = json.loads(value)
                                    result_except[key] = value
                                except:
                                    value = value



                        except:
                            self.logger.info(
                                "{result_except}中{ value}非合法字典格式。接口取值未处理".format(result_except=result_except,
                                                                                 value=value))

                    # sql处理第二步
                    if type(value) == str:
                        if (value.lower().startswith(('select', 'update', 'insert', 'delete'))) and (
                                value.lower() != 'select') and (value.lower() != 'update') and (
                                value.lower() != 'insert') and (value.lower() != 'delete'):
                            db = comdb.db()
                            try:
                                values_key = list(db.excute(value).values())

                                if value.lower().startswith('select'):
                                    if '|' in key:
                                        list_keys = key.split('|')
                                        for key_one in list_keys:
                                            result_return = dict(result_return,
                                                                 **{key_one: values_key[list_keys.index(key_one)]})
                                    else:
                                        result_return = dict(result_return, **{key: values_key[0]})
                                # else:
                                #     result_return = dict(result_return, **{key: None})



                            except:
                                if '|' in key:
                                    list_keys = key.split('|')
                                    for key_one in list_keys:
                                        result_return = dict(result_return, **{key_one: None})
                                else:
                                    result_return = dict(result_return, **{key: None})

                # mongodb第二部
                if ( ["mongodb_type", "mongodb_table", "mongodb_query",
                                                                       "mongodb_order",
                                                                       "mongodb_result"] in list(result_except.keys())) or ( ["mongodb_type", "mongodb_table", "mongodb_query",
                                                                       "mongodb_order",
                                                                       "mongodb_result"] == list(result_except.keys())) :
                    db = comdb.db()
                    result_mongodb = db.mongoDB_excute(result_except["mongodb_table"],
                                                                           result_except["mongodb_type"],
                                                                           result_except["mongodb_query"],
                                                                           result_except["mongodb_result"],
                                                                           sorts=result_except["mongodb_order"])
                    if result_mongodb:
                       result_return = dict(result_return, **result_mongodb)

        else:
            print('接口执行失败，取返回值为空')
            for key, value in result_except.items():
                result_return[key] = None






        #参数与取值组成dict返回

        return result_return





    def paramUnique(self,paramx):
        '''参数要求唯一性时，对参数进行处理'''

        if type(paramx)==str:
            paramx = paramx.replace('{$unique}', com.unique())
            self.logger.debug("参数转换后:%s" % str(paramx))


        return paramx


    def getData_file(self,file):
        '''上传文件类接口，参数处理'''

        f=open(r'./TestFile/%s'%file,"rb")
        # path = os.path.join(os.getcwd(), 'testFile\%s' % file)
        # f=open(path, "rb")
        # m={
        #     "file": ("%s" % file,
        #              f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        #              )
        # }
        if (file.endswith(".jpg")) or (file.endswith(".jpeg")):
            file_type = "image/jpeg"
        elif (file.endswith(".xlsx")) or (file.endswith(".xls")):
            file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif file.endswith(".epub"):
            file_type ="application/epub"
        m = {
            "file": ("%s" % file, f, file_type)
        }

        m = MultipartEncoder(m)

        self.header["Content-Type"] = m.content_type

        data = m




        # f.close()
        return data

    def getData_filex(self,file):
        '''上传文件类接口，参数处理'''

        f=open(r'./TestFile/%s'%file,"rb")
        # path = os.path.join(os.getcwd(), 'testFile\%s' % file)
        # f=open(path, "rb")
        m={
            "file": ("%s" % file,
                     f, "application/epub"
                     )
        }
        m1={"title": "", "author": "", "categoryIds": "1", "cover": "", "paperPrice": "1", "price": "2", "publisher": "", "isbn": "", "wordCount": "200", "startTime": "2021-08-24", "endTime": "2021-08-26", "publishDate": "", "copyright": "授权说明", "description": "<p>test</p><p>test</p><p><br/></p>", "baseUsers": "200", "status": "ON"}
        m=dict(m,**m1)
        # if (file.endswith("jpg")) or (file.endswith("jpeg")):
        #     file_type = "image/jpeg"
        # elif (file.endswith("xlsx")) or (file.endswith("xls")):
        #     file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        # m = {
        #     "file": ("%s" % file, f, file_type)
        # }

        m = MultipartEncoder(m)

        self.header["Content-Type"] = m.content_type

        data = m




        # f.close()
        return data

    def paramFile(self,bodyParam,fileParam):
        '''上传文件类接口的参数处理'''
        # f = open(fileParam, "rb")
        # self.logger.info(fileParam)
        f = open(r'./{filepath}'.format(filepath=fileParam), "rb")
        # path = os.path.join(os.getcwd(), 'testFile\%s' % file)
        # f=open(path, "rb")
        # m={
        #     "file": ("%s" % file,
        #              f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        #              )
        # }
        if (fileParam.endswith(".jpg")) or (fileParam.endswith(".jpeg")):
            file_type = "image/jpeg"
        elif (fileParam.endswith(".xlsx")) or (fileParam.endswith(".xls")):
            file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif fileParam.endswith(".epub"):
            file_type = "application/epub"
        m = {
            "file": ("%s" % fileParam.split("saas/saas_program/testFile/")[1], f, file_type)
        }



        if (bodyParam!=None) and (bodyParam!=''):
            # self.logger.info(type(bodyParam))
            if type(bodyParam) == str:
                bodyParam = com.textTojson(bodyParam)
                # self.logger.info(type(bodyParam))

            if (type(bodyParam) == str) and (bodyParam != ''):
                bodyParam = json.loads(bodyParam)
                # self.logger.info(type(bodyParam))

            # self.logger.info(type(bodyParam))
            # self.logger.info(bodyParam)

            m = dict(m, **bodyParam)

        m = MultipartEncoder(m)

        self.header["Content-Type"] = m.content_type

        data = m

        return data





    def dataEncode(self,data):
        '''接口传参body包含中文时，转换参数'''

        if (data != '')and (type(data)==str):
            data = data.encode('utf-8')
        return data

    def paramTransmission(self,paramx,value):
        '''接口参数非固定值时，动态参数传入。例：{id}'''
        # self.logger.info("参数：%s"%str(paramx))
        # self.logger.info("入参值：%s" % str(value))
        if value != None:
            if not re.search('{mongoDB:.*}',paramx):
                paramx = re.sub('{[0-9A-Za-z_.:]+}', str(value), paramx)
        # self.logger.info("入参后：%s"%str(paramx))
        return paramx



    def paramTransmissionFull(self,paramx, value_dict):
        self.logger.debug('paramTransmissionFull处理前参数{param}'.format(param=paramx))
        self.logger.debug('paramTransmissionFull处理前被入数据值{param}'.format(param=value_dict))
        if (paramx==None) or (paramx==''):
            paramx_new=paramx
        else:
            if (value_dict == None) or (value_dict == {}) or (value_dict == '') :
                paramx_new = paramx
            else:
                for key, value in value_dict.items():
                    if type(paramx) == dict:
                        paramx_new = re.sub('\{(%s)\}' % key, str(value), json.dumps(paramx))
                        paramx_new = json.loads(paramx_new)
                    elif type(paramx) == str:
                        paramx_new = re.sub('\{(%s)\}' % key, str(value), paramx)
                    paramx = paramx_new

        self.logger.debug('paramTransmissionFull处理后参数{param}'.format(param=paramx_new))
        return paramx_new
    # def paramTransmissionFull(self,paramx, value_dict):
    #     '''精确入参数，如url:file/{fileId} ，用{“fileId”:1} 转换成file/1
    #     参数中{"id":"{id}"}, 用{"id":1} 转换成参数{"id":1}
    #     '''
    #     self.logger.debug("paramTransmissionFull处理前参数{data}及类型{type}".format(data=str(paramx),
    #                                                                       type=type(paramx)))
    #     self.logger.debug("paramTransmissionFull处理前入参值：%s" % str(value_dict))
    #     param_new_dict = {}
    #     for key, value in value_dict.items():
    #         if type(paramx) == dict:
    #             for param_key, param_value in paramx.items():
    #                 param_value = str(param_value).replace('{' + key + '}', str(value))
    #                 param_new_dict[param_key] = param_value
    #             param_new = param_new_dict
    #
    #         elif type(paramx) == str:
    #             try:
    #                 paramx = json.loads(paramx)
    #                 param_new = self.paramTransmissionFull(paramx, value_dict)
    #             except:
    #                 param_new = paramx.replace('{' + key + '}', str(value))
    #
    #     self.logger.debug("paramTransmissionFull处理后{data}及类型{type}".format(data=str(param_new),
    #                                                                          type=type(param_new)))
    #
    #     return param_new


    def param_SQL(self,paramx,sql):
        '''执行sql，并取值入参数'''
        # self.logger.info('sql执行前参数：%s'%paramx)
        # self.logger.info('sql执行前参数：%s' % type(paramx))



        if (type(paramx)==dict) and (paramx!=None):

            db = comdb.db()
            # db.connect()
            values = db.excute(sql)

            db.close()
            paramx=com.jsonTotext(paramx)
            if values==None:
                self.logger.info("%s"%sql)
            else:
                for k, v in values.items():
                    paramx = paramx.replace('{sql:%s}' % k, str(v))

            paramx=com.textTojson(paramx)

        elif (type(paramx)==str) and (paramx!=''):
            db = comdb.db()
            # db.connect()
            values = db.excute(sql)
            db.close()
            if values==None:
                self.logger.info("%s取值为空"%sql)
            else:
                for k, v in values.items():
                    paramx = paramx.replace('{sql:%s}' % k, str(v))

        # self.logger.info('sql执行后参数：%s' % paramx)

        return paramx




    def param_time(self,paramx):
        '''用例中参数值捕获nowtime标识，转化成当前时间数据'''
        # self.logger.info(type(paramx))

        # self.logger.info(paramx)
        if  (type(paramx) == str) and (paramx != ''):

            paramx = json.loads(paramx)



            if type(paramx) == dict:
                paramx=paramx
            else:
                paramx=json.dumps(paramx)
        if (type(paramx) == dict) and (paramx != None):
            for k, v in paramx.items():
                if 'nowtime' in str(v):
                    if v == 'nowtime':
                        paramx[k] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
                    else:
                        # delta = datetime.timedelta(days=3)
                        # n_days = now + delta

                        # nowtime = datetime.datetime.now()
                        # paramx[k] = datetime.datetime.strftime(eval(v), "%Y-%m-%d %H:%M:%S")
                        v=str(v)
                        def f(x):
                            x = str(x.group())
                            nowtime = datetime.datetime.now()
                            return datetime.datetime.strftime(eval(x), "%Y-%m-%d %H:%M:%S")

                        paramx[k]  = re.sub('nowtime[0-9A-Za-z+-.()=]+', f, v)


            paramx = json.dumps(paramx)


        return paramx


    def param_time_new(self,paramx):
        '''用例中参数值捕获nowtime标识，转化成当前时间数据'''
        # self.logger.info(type(paramx))

        # self.logger.info(paramx)
        if  (type(paramx) == str) and (paramx != ''):

            paramx = json.loads(paramx)



            if type(paramx) == dict:
                paramx=paramx
            else:
                paramx=json.dumps(paramx)
        if (type(paramx) == dict) and (paramx != None):
            for k, v in paramx.items():
                if 'nowtime' in str(v):
                    if v == 'nowtime':
                        paramx[k] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
                    else:
                        # delta = datetime.timedelta(days=3)
                        # n_days = now + delta

                        # nowtime = datetime.datetime.now()
                        # paramx[k] = datetime.datetime.strftime(eval(v), "%Y-%m-%d %H:%M:%S")
                        v=str(v)
                        def f(x):
                            x = str(x.group())
                            nowtime = datetime.datetime.now()
                            return datetime.datetime.strftime(eval(x), "%Y-%m-%d %H:%M:%S")

                        paramx[k]  = re.sub('nowtime[0-9A-Za-z+-.()=]+', f, v)


            paramx = json.dumps(paramx)


        return paramx




    def param_redis(self, paramx, redis):
        '''执行sql，并取值入参数'''
        # self.logger.info('sql执行前参数：%s'%paramx)
        # self.logger.info('sql执行前参数：%s' % type(paramx))

        if (type(paramx) == dict) and (paramx != None):

            db = comdb.db()
            if type(redis)==dict:
                values = db.redis_excute(db=redis["db"],method=redis["method"],key=redis["key"],key_type=redis["key_type"])
            elif type(redis)==str:
                redis=json.loads(redis)
                values = db.redis_excute(db=redis["db"], method=redis["method"], key=redis["key"],
                                         key_type=redis["key_type"])


            paramx = com.jsonTotext(paramx)
            if values == None:
                self.logger.debug("redis取值为空")
            else:
                for k, v in values.items():
                    paramx = paramx.replace('{sql:%s}' % k, str(v))

            paramx = com.textTojson(paramx)

        elif (type(paramx) == str) and (paramx != ''):
            db = comdb.db()
            db = comdb.db()
            if type(redis) == dict:
                values = db.redis_excute(db=redis["db"], method=redis["method"], key=redis["key"],
                                         key_type=redis["key_type"])
            elif type(redis) == str:
                redis = json.loads(redis)
                values = db.redis_excute(db=redis["db"], method=redis["method"], key=redis["key"],
                                         key_type=redis["key_type"])
            if values == None:
                self.logger.debug("redis取值为空")
            else:
                for k, v in values.items():
                    paramx = paramx.replace('{sql:%s}' % k, str(v))

        # self.logger.info('redis执行后参数：%s' % paramx)

        return paramx

    def param_mongoDB(self, paramx, mongoDB,mongodb_front=None):
        '''执行mongodb，并取值入参数'''
        # self.logger.info('sql执行前参数：%s'%paramx)
        # self.logger.info('sql执行前参数：%s' % type(paramx))

        if (type(paramx) == dict) and (paramx != None):

            db = comdb.db()
            if type(mongoDB) == dict:
                values = db.mongoDB_excute(table=mongoDB["table"], method=mongoDB["method"],
                                           condition=mongoDB["condition"],
                                           results=mongoDB["result"],condition_value=mongodb_front,sorts=mongoDB["order"])
            elif type(mongoDB) == str:
                mongoDB = json.loads(mongoDB)
                values = db.mongoDB_excute(table=mongoDB["table"], method=mongoDB["method"],
                                           condition=mongoDB["condition"],
                                           results=mongoDB["result"],condition_value=mongodb_front,sorts=mongoDB["order"])

            paramx = com.jsonTotext(paramx)
            if values == None:
                self.logger.debug("mongoDB取值为空")
            else:
                for k, v in values.items():
                    paramx = paramx.replace('{mongoDB:%s}' % k, str(v))

            paramx = com.textTojson(paramx)

        elif (type(paramx) == str) and (paramx != ''):
            db = comdb.db()
            if type(mongoDB) == dict:
                values = db.mongoDB_excute(table=mongoDB["table"], method=mongoDB["method"],
                                           condition=mongoDB["condition"],
                                           results=mongoDB["result"],condition_value=mongodb_front,sorts=mongoDB["order"])
            elif type(mongoDB) == str:
                mongoDB = json.loads(mongoDB)
                values = db.mongoDB_excute(table=mongoDB["table"], method=mongoDB["method"],
                                           condition=mongoDB["condition"],
                                           results=mongoDB["result"],condition_value=mongodb_front,sorts=mongoDB["order"])
            if values == None:
                self.logger.debug("mongoDB取值为空")
            else:
                for k, v in values.items():
                    paramx = paramx.replace('{mongoDB:%s}' % k, str(v))

        # self.logger.info('redis执行后参数：%s' % paramx)

        return paramx



    # def param_frontapi(self,case):
    #     '''执行前置接口，进行参数处理'''
    #     if case["frontCase"] != '':
    #         self.logger.debug("需要调用前置接口")
    #         case["frontCase"] = json.loads(case["frontCase"])
    #         value = interface.frontapi_exucte(case["frontCase"]["frontApi"], case["frontCase"]["resulctParam"])
    #         case["url_params"] = Http.paramTransmission(case["url_params"], value)
    #         case["url"] = Http.paramTransmission(case["url"], value)
    #         case["body_params"] = Http.paramTransmission(case["body_params"], value)
    #
    #
    #         if (case["mongoDB"] != '') and (value):
    #             if type(case["mongoDB"]) == str:
    #                 case["mongoDB"] = json.loads(case["mongoDB"])
    #             frontapiMongo = False
    #             for v in list(case["mongoDB"]["condition"].values()):
    #                 if re.search('{frontApi}', str(v)):
    #                     frontapiMongo = True
    #             if frontapiMongo:
    #                 case["body_params"] = Http.param_mongoDB(case["body_params"], case['mongoDB'], value)
    #                 case["url_params"] = Http.param_mongoDB(case["url_params"], case['mongoDB'], value)
    #                 case["url"] = Http.param_mongoDB(case["url"], case['mongoDB'], value)















