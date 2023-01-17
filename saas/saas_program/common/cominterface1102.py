from saas.saas_program import  readConfig
from saas.saas_program.common import xlsxRead,runCase1102
import logging
import json
logging.basicConfig(level=logging.INFO)

import ast
class interface():
    def __init__(self,Http,log_cap,caseName=None):
        self.results = []
        '''调用前置接口，取需要入参值'''

        self.addResults = {}
        '''调用前置接口，新增数据值（需要删除）'''

        self.logger = logging.getLogger(caseName)
        self.log_cap=log_cap
        ch = logging.StreamHandler(self.log_cap)
        ch.setLevel(logging.DEBUG)
        myfmt = logging.Formatter(
            '%(asctime)s - %(name)s: %(message)s')
        ch.setFormatter(myfmt)
        self.logger.addHandler(ch)

        self.loggername = caseName
        self.Http =Http
        # self.Http = configHttp.Http(self.loggername)

    def front_value_excute(self,case, result_frontCase):
        '''执行前置函数后，对数据的处理'''
        # result_frontCase.pop('result_http')
        # result_frontCase.pop('casename')

        # 前置执行后，直接取值入参
        case["url_params"] = self.Http.paramTransmissionFull(case["url_params"], result_frontCase)
        case["url"] = self.Http.paramTransmissionFull(case["url"], result_frontCase)
        case["body_params"] = self.Http.paramTransmissionFull(case["body_params"], result_frontCase)

        # 前置执行后，执行MongoDB操作，然后入参，待修改
        # if (case["mongoDB"] != '') and (value):
        #     frontapiMongo = False
        #     if type(case["mongoDB"]) == str:
        #         case["mongoDB"] = json.loads(case["mongoDB"])
        #     for v in list(case["mongoDB"]["condition"].values()):
        #         if re.search('{frontApi}', str(v)):
        #             frontapiMongo = True
        #     if frontapiMongo:
        #         case["body_params"] = self.Http.param_mongoDB(case["body_params"], case['mongoDB'], value)
        #         case["url_params"] = self.Http.param_mongoDB(case["url_params"], case['mongoDB'], value)
        #         case["url"] = self.Http.param_mongoDB(case["url"], case['mongoDB'], value)
    def frontapi_exucte(self,casebase):
        '''执行前置接口，不传参，取返回结果：如调用创建数据接口'''






        file = readConfig.get_testFile()
        sheet = readConfig.get_testSheet()
        casesClass = xlsxRead.casesRead(file, sheet)

        if casebase["frontCase"] != '':
            # [{"frontApi":"接口a","id":"id"}]
            for frontcase in   ast.literal_eval(casebase["frontCase"]):
                self.logger.debug('frontcase值{a}'.format(a=str(frontcase)))
                self.logger.debug('frontcase类型{a}'.format(a=str(type(frontcase))))

                frontcase_dict = frontcase
                frontcase_api = frontcase_dict["frontApi"]
                frontcase_dict.pop("frontApi")
                result_cominterface_need=frontcase_dict

                if frontcase_api != None:
                    case = casesClass.get_one_caseByName(frontcase_api)

                    front_front_interface = casesClass.get_frontCase(case)
                    self.logger.debug(str(case))

                    # Http = configHttp.Http()
                    # self.Http.getauth()

                    if front_front_interface != '':
                        self.results=self.frontapi_exucte(case)

                    if result_cominterface_need=={}:
                        # if case["lastCase"]!='':

                        http_case = runCase1102.runOneCase(case,self.Http)
                    else:
                        http_case = runCase1102.runOneCase(case,self.Http,result_cominterface_need)


                    # self.logger.info("执行前置：%s" % str(case["name"]))
                    # self.logger.info("前置url：%s" % str(http_case["result_http"].request.url))
                    # self.logger.info("前置body：%s" % str(http_case["result_http"].request.body))
                    # self.logger.info("前置method：%s" % str(http_case["result_http"].request.method))
                    # try:
                    #     self.logger.info("前置接口%s返回：%s" % (str(case["name"]), str(http_case["result_http"].json())))
                    # except:
                    #     self.logger.info("前置接口%s返回：%s" % (str(case["name"]), str(http_case["result_http"].content)))
                    self.logger.debug("前置执行前case情况{case}".format(case=str(casebase)))

                    self.front_value_excute(casebase,http_case.get("result_next_parm"))
                    self.logger.debug("前置执行并处理后当前case情况{case}".format(case=str(casebase)))

                    self.results.append(http_case.get("result_lasecase_parm"))












        return self.results

    # def lastapi_exucte(self,last_inter_name, para):
    #     '''执行后置接口，需传参，不取返回结果：如调用删除接口'''
    #     # print(last_inter_name)
    #     # print(para)
    #     file = readConfig.get_testFile()
    #     sheet = readConfig.get_testSheet()
    #     casesClass = xlsxRead.casesRead(file, sheet)
    #     if last_inter_name != None:
    #         case = casesClass.get_one_caseByName(last_inter_name)
    #         if para != None:
    #
    #             if last_inter_name != None:
    #                 case = casesClass.get_one_caseByName(last_inter_name)
    #
    #                 data_file = casesClass.get_file(case)
    #
    #                 # Http = configHttp.Http()
    #                 self.Http.getauth()
    #
    #                 case["url_params"] = self.Http.paramTransmission(case["url_params"], para)
    #                 case["url"] = self.Http.paramTransmission(case["url"], para)
    #                 case["body_params"] = self.Http.paramTransmission(case["body_params"], para)
    #
    #                 case["url_params"] = self.Http.paramUnique(case["url_params"])
    #                 case["body_params"] = self.Http.paramUnique(case["body_params"])
    #                 case["url"] = self.Http.paramUnique(case["url"])
    #
    #                 # if case["body_params"] != '':
    #                 #     case["body_params"] = case["body_params"].encode('utf-8')
    #                 if data_file != '':
    #                     case["body_params"] = self.Http.getData_file(data_file)
    #                 # case["body_params"] = Http.get_urlParams_addtoken(case['method'], case["body_params"])
    #                 # case["url_params"] = Http.get_urlParams_addtoken(case['method'], case["url_params"])
    #                 #
    #                 # # 仅鸿蒙后台设置
    #                 # if os.environ["platform"] == "后台":
    #                 #     case["body_params"] = Http.get_urlParams_addUserToken(case["body_params"])
    #                 #     case["url_params"] = Http.get_urlParams_addUserToken(case["url_params"])
    #
    #                 #后置接口的参数来源应由原用例的结果（取值或sql）填充，暂不考虑来源于后置直接执行sql
    #                 # if case['sql'] != '':
    #                 #     case["body_params"] = Http.param_SQL(case["body_params"], case['sql'])
    #                 #     case["url_params"] = Http.param_SQL(case["url_params"], case['sql'])
    #                 #     case["url"] = Http.param_SQL(case["url"], case['sql'])
    #
    #                 case["body_params"] = self.Http.dataEncode(case["body_params"])
    #                 http_case = self.Http.execute(case["url"], case["method"], case["url_params"], case["body_params"])
    #                 # self.logger.debug(http_case.request.headers)
    #                 # self.logger.debug(http_case.request.body)
    #                 # self.logger.debug(http_case.request.method)
    #                 # self.logger.debug("后置接口返回：%s" % str(http_case.json()))
    #                 if self.Http.assertResult(http_case, case):
    #                     self.logger.info("后置接口%s执行成功%s"%(str(case["name"]),str(para)))
    #                 else:
    #                     self.logger.info("执行后置：%s" % str(case["name"]))
    #                     self.logger.info("后置url：%s" % str(http_case.request.url))
    #                     self.logger.info("后置body：%s" % str(http_case.request.body))
    #                     self.logger.info("后置method：%s" % str(http_case.request.method))
    #                     try:
    #                         self.logger.info("后置接口%s返回：%s" % (str(case["name"]),str(http_case.json())))
    #                     except:
    #                         self.logger.info("后置接口%s返回：%s" % (str(case["name"]),str(http_case.content)))
    #                     self.logger.info("后置接口%s执行失败"%(str(case["name"])))
    #         else:
    #             self.logger.info("执行后置的接口%s时未传参，则不执行该后置接口" % case["name"])


    def lastapi_exucte(self,basecase,results):
        '''执行后置接口'''

        file = readConfig.get_testFile()
        sheet = readConfig.get_testSheet()
        casesClass = xlsxRead.casesRead(file, sheet)

        if basecase["lastCase"]!='':
            self.logger.debug('basecase["lastCase"]内容{frontcase}类型{type}'.format(frontcase=str(basecase["lastCase"]), type=type(basecase["lastCase"])))
            if type(basecase["lastCase"])!=dict:
                basecase["lastCase"]=json.loads(basecase["lastCase"])
            case = casesClass.get_one_caseByName(basecase["lastCase"]["lastApi"])

            # result_case=False
            for result in results:
                if result != None:
                    if case["name"] == result["lastApi"]:
                        result.pop("lastApi")
                        self.front_value_excute(case, result)
                        result_case=self.Http.assertResult(runCase1102.runOneCase(case,self.Http)["result_http"],case)
                        if not result_case:
                            self.logger.info("执行后置接口{name}失败".format(name=case["name"]))
                        results.remove(result)







        if basecase["frontCase"]!='':
            for frontcase in ast.literal_eval(basecase["frontCase"]):
                logging.debug('frontcase内容{frontcase}类型{type}'.format(frontcase=frontcase,type=type(frontcase)))
                frontcase=casesClass.get_one_caseByName(frontcase["frontApi"])
                self.lastapi_exucte(frontcase,results)




























