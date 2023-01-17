from saas.saas_program import readConfig
from  saas.saas_program.common import xlsxRead
from saas.models import  *
import logging
import  json
from saas.saas_program.common import cominterface1202
import re
logging.basicConfig(level=logging.INFO)
import threading
from collections import  Counter

lock = threading.Lock()

def runOneCase(case,Http,result_datas=None):

    # file = readConfig.get_testFile()
    # sheet = readConfig.get_testSheet()
    # casesClass = xlsxRead.casesRead(file, sheet)



    Http=Http
    logger = logging.getLogger(Http.log_name)
    # Http.getauth()


    case["body_params"] = Http.param_time(case["body_params"])
    logger.debug("执行Http.param_time后body_params内容{body}及类型{type}".format(body=case["body_params"],type=type(case["body_params"])))
    case["url_params"] = Http.paramUnique(case["url_params"])
    case["body_params"] = Http.paramUnique(case["body_params"])
    logger.debug("执行Http.paramUnique后body_params内容{body}及类型{type}".format(body=case["body_params"],type=type(case["body_params"])))

    # logger.info(case["body_params"])

    case["url"] = Http.paramUnique(case["url"])






    # if case["cookies"] != '':
    #     if case["cookies"] != '不登录':
    #         case["cookies"] = json.loads(case["cookies"])
    #     else:
    #         case["cookies"] = '不登录'
    # else:
    #     case["cookies"] = None











    # logger.info(case)



    #后面应该有用
    # if case['sql']!='':
    #     case["body_params"] = Http.param_SQL(case["body_params"],case['sql'])
    #     logger.debug("执行Http.param_SQL后body_params内容{body}及类型{type}".format(body=case["body_params"],type=type(case["body_params"])))
    #     case["url_params"] = Http.param_SQL(case["url_params"],case['sql'])
    #     case["url"] = Http.param_SQL(case["url"], case['sql'])

    # if case["redis"]!='':
    #     case["body_params"] = Http.param_redis(case["body_params"], case['redis'])
    #     logger.debug("执行Http.param_redis后body_params内容{body}及类型{type}".format(body=case["body_params"],type=type(case["body_params"])))
    #     case["url_params"] = Http.param_redis(case["url_params"], case['redis'])
    #     case["url"] = Http.param_redis(case["url"], case['redis'])

    # if case["mongoDB"] != '':
    #     if type(case["mongoDB"])==str:
    #         case["mongoDB"]=json.loads(case["mongoDB"])
    #     frontapiMongo=False
    #     for v in list(case["mongoDB"]["condition"].values()):
    #         if re.search('{frontApi}', str(v)):
    #             frontapiMongo=True
    #     if not frontapiMongo:
    #         case["body_params"] = Http.param_mongoDB(case["body_params"], case['mongoDB'])
    #         logger.debug("执行Http.param_mongoDB后body_params内容{body}及类型{type}".format(body=case["body_params"],type=type(case["body_params"])))
    #
    #         case["url_params"] = Http.param_mongoDB(case["url_params"], case['mongoDB'])
    #         case["url"] = Http.param_mongoDB(case["url"], case['mongoDB'])


    # logger.info(case)
    # logger.info(case["body_params"])





    # if data_file != '':
    #     # print(case["body_params"])
    #     if case["body_params"]!='':
    #         if type(case["body_params"])==str:
    #             case["body_params"]=com.textTojson(case["body_params"])
    #         if (type(case["body_params"]) == str) and (case["body_params"] != ''):
    #             case["body_params"] = json.loads(case["body_params"])
    #
    #         params={}
    #         # print(type(case["body_params"]))
    #         # print(case["body_params"])
    #         for k, v in case["body_params"].items():
    #             params[k]=(None,v)
    #     else:
    #         params={}
    #     case["body_params"]=dict(Http.getData_file(data_file),**params)
    #     # case["body_params"] = Http.getData_file(data_file)
    # data_file = casesClass.get_file(case)
    if case["file"]:
        case["body_params"]=Http.paramFile(case["body_params"],case["file"])
        logger.debug("执行Http.paramFile后body_params内容{body}及类型{type}".format(body=case["body_params"],type=type(case["body_params"])))



    case["body_params"] = Http.dataEncode(case["body_params"])


    logger.debug("执行Http.dataEncode后body_params内容{body}及类型{type}".format(body=case["body_params"],type=type(case["body_params"])))

    #取值不执行sql的请求可以不加锁，待加上
    lock.acquire()
    try:
        try:

           http_case = Http.execute(case["url"], case["method"], case["url_params"], case["body_params"])

           try:
               logger.debug('case内容{case}和类型{type}'.format(case=case, type=type(case)))

               logger.info("执行接口：%s" % str(case["information"]))
               # logger.info("执行接口header：%s" % str(http_case.request.headers))
               logger.info("请求路径：%s" % str(http_case.request.url))
               logger.info("请求参数：%s" % str(http_case.request.body))
               logger.info("请求方法：%s" % str(http_case.request.method))
               logger.info("返回码：%s" % str(http_case.status_code))

               logger.info("接口【%s】 返回内容：%s" % (str(case["information"]), str(http_case.json())))
           except:
               logger.info("接口【%s】 返回内容：%s" % (str(case["information"]), str(http_case.content)))
        except:
            logger.debug('case内容{case}和类型{type}'.format(case=case, type=type(case)))
            logger.info("执行接口：%s" % str(case["information"]))
            logger.info("请求路径：%s" % str(http_case.request.url))
            logger.info("请求参数：%s" % str(http_case.request.body))
            logger.info("请求方法：%s" % str(http_case.request.method))
            logger.info("返回码：%s" % str(http_case.status_code))

            logger.info("执行用例{case}报错".format(case=case["information"]))







        result = {"result_http": http_case}


        logger.debug(result_datas)
        if result_datas != None:
            try:
                x=Http.getResult(http_case, case, result_datas)
                result_next_parm = {"result_next_parm": x}
            except:
                result_next_parm = {"result_next_parm":None}
            result = dict(result, **result_next_parm)

        relations_last = relationship.objects.filter(status=True,basecase_id=case["id"], type=1)
        if relations_last.exists():
            try:
                case_last = relations_last[0].relatedcase
                result_last_need=cominterface1202.get_result_cominterface_need(relations_last[0])
                # result_last_need = relations_last[0].dealcontent

                case["lastCase"] = {"lastApi":case_last.id,**result_last_need}
                result_lasecase_parm = {"result_lasecase_parm": Http.getResult(http_case, case, case["lastCase"])}
            except:
                result_lasecase_parm = {"result_lasecase_parm":None}
            result = dict(result, **result_lasecase_parm)

        # try:
        #     logger.info("接口{case}返回内容dict{result}".format(case=case["name"], result=str(result)))
        # except:
        #     logger.info("接口{case}获取返回值执行失败".format(case=case["name"]))
        logger.info("接口{case}返回内容{result}".format(case=case["information"], result=str(result)))


    except:
        result= {"result_http":None}
        if result_datas != None:
            result_next_parm = {"result_next_parm": None}
            result = dict(result, **result_next_parm)
        if case["lastCase"] != '':
            result_lasecase_parm = {"result_lasecase_parm": None}
            result = dict(result, **result_lasecase_parm)



        logger.info("接口{case}返回内容{result}".format(case=case["information"], result=str(result)))

    finally:
        lock.release()

    if case["file"]:
        Http.header["Content-Type"] = readConfig.get_header()["Content-Type"]









    return result






