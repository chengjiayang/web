from saas.saas_program import  readConfig
from saas.saas_program.common import xlsxRead,runCase1102
import logging
import json
logging.basicConfig(level=logging.INFO)
from saas.models import  *
import ast
from django.forms.models import model_to_dict


def get_result_cominterface_need(relation):
    dealtype = relation.get_dealtype_display()
    if 'mongodb' in dealtype:
        m_type = relation.get_m_type_display()
        m_table = relation.m_table
        m_query = relation.m_query
        if m_query != None:
            try:
                m_query = json.loads(m_query)
            except:
                m_query = m_query
        else:
            m_query = {}
        m_order = relation.m_order
        if m_order != None:
            try:
                m_order = json.loads(m_order)
            except:
                m_order = m_order
        m_result = relation.m_result
        if m_result != None:
            try:
                m_result = json.loads(m_result)
            except:
                m_result = m_result

        result_cominterface_need = {"mongodb_type": m_type,
                                    "mongodb_table": m_table,
                                    "mongodb_query": m_query,
                                    "mongodb_order": m_order,
                                    "mongodb_result": m_result,
                                    }

    elif '接口返回' in dealtype:
        interfaceProcess = relation.interfaceProcess
        if (type(interfaceProcess) == str) and (interfaceProcess != ''):
            try:
                interfaceProcess = json.loads(interfaceProcess)
            except:
                interfaceProcess = interfaceProcess

        result_cominterface_need = interfaceProcess

    elif '接口query请求' in dealtype:
        interfaceProcess = relation.interfaceProcess

        if (type(interfaceProcess) == str) and (interfaceProcess!=''):
            try:
                interfaceProcess = json.loads(interfaceProcess)
                interfaceProcess=dict(interfaceProcess,**{"to":"request_urlparam"})
            except:
                interfaceProcess=interfaceProcess

        result_cominterface_need = interfaceProcess

    elif '接口body请求' in dealtype:
        interfaceRequest_body = relation.interfaceRequest_body

        if (type(interfaceRequest_body) == str) and (interfaceRequest_body!=''):
            try:
                interfaceRequest_body = json.loads(interfaceRequest_body)
                interfaceRequest_body=dict(interfaceRequest_body,**{"to":"request_bodyparam"})
            except:
                interfaceRequest_body=interfaceRequest_body

        result_cominterface_need = interfaceRequest_body

    elif 'sql' in dealtype:
        sqls = relation.sqls
        if (type(sqls) == str) and (sqls!=''):
            try:
                sqls = json.loads(sqls)
            except:
                sqls=sqls
        result_cominterface_need = sqls


    elif '无' in dealtype:
        result_cominterface_need = None

    return result_cominterface_need

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
        # self.relations_front=None
        # self.case=None
        # self.relations_front_front=None
        # self.result_cominterface_need=None


        relations_front=relationship.objects.filter(status=True,basecase_id=casebase["id"],type=0)

        if relations_front.exists():
            for relation_front in   relations_front:
                # self.logger.debug('frontcase值{a}'.format(a=str(frontcase)))
                # self.logger.debug('frontcase类型{a}'.format(a=str(type(frontcase))))

                case = relation_front.relatedcase
                try:
                    file = case.file.url
                except:
                    file = None
                case.method = case.get_method_display()
                case = model_to_dict(case)
                case["file"]=file

                # result_cominterface_need = relation_front.dealcontent


                # Http = configHttp.Http()
                # self.Http.getauth()

                relations_front_front = relationship.objects.filter(status=True,basecase_id=case["id"], type=0)
                if relations_front_front.exists():
                    self.results = self.frontapi_exucte(case)




                result_cominterface_need=get_result_cominterface_need(relation_front)



                if not result_cominterface_need:
                    http_case = runCase1102.runOneCase(case, self.Http)
                else:
                    http_case = runCase1102.runOneCase(case, self.Http, result_cominterface_need)

                # self.logger.info("执行前置：%s" % str(case["name"]))
                # self.logger.info("前置url：%s" % str(http_case["result_http"].request.url))
                # self.logger.info("前置body：%s" % str(http_case["result_http"].request.body))
                # self.logger.info("前置method：%s" % str(http_case["result_http"].request.method))
                # try:
                #     self.logger.info("前置接口%s返回：%s" % (str(case["name"]), str(http_case["result_http"].json())))
                # except:
                #     self.logger.info("前置接口%s返回：%s" % (str(case["name"]), str(http_case["result_http"].content)))
                self.logger.debug("前置执行前case情况{case}".format(case=str(casebase)))

                self.front_value_excute(casebase, http_case.get("result_next_parm"))
                self.logger.debug("前置执行并处理后当前case情况{case}".format(case=str(casebase)))

                self.results.append(http_case.get("result_lasecase_parm"))



        return self.results




    def lastapi_exucte(self,basecase,results):
        '''执行后置接口'''

        relations_last = relationship.objects.filter(status=True,basecase_id=basecase["id"], type=1)



        if relations_last.exists():
            case = relations_last[0].relatedcase
            case.method = case.get_method_display()
            case = model_to_dict(case)

            for result in results:
                if result != None:
                    if case["id"] == result["lastApi"]:
                        result.pop("lastApi")
                        self.front_value_excute(case, result)
                        result_case=self.Http.assertResult(runCase1102.runOneCase(case,self.Http)["result_http"],case)
                        if not result_case:
                            self.logger.info("执行后置接口{name}失败".format(name=case["name"]))
                        results.remove(result)
                        break



        relations_fronts = relationship.objects.filter(status=True,basecase_id=basecase["id"], type=0)
        if relations_fronts.exists():
            for relation_front in relations_fronts:
                frontcase = relation_front.relatedcase
                frontcase.method = frontcase.get_method_display()
                frontcase = model_to_dict(frontcase)
                self.lastapi_exucte(frontcase,results)




















































