

import logging
from saas.saas_program import readConfig
from saas.saas_program.common import xlsxRead,configHttp,com,cominterface1102,runCase1102
import unittest
from ddt import data, ddt
logging.basicConfig(level=logging.INFO)
from io import StringIO

# import os, sys
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 定位到你的django根目录
# sys.path.append(os.path.abspath(os.path.join(BASE_DIR, os.pardir)))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_tasks.settings")  # 你的django的settings文件
#
# from saas.models import cases,Project

# len = list(range(0, 11))
# @ddt
class TestCasecamp13(unittest.TestCase):
    # @data(*len)
    def test_camp13(self):
        '训练营管理接口_编辑训练营:camp13'
        logger = logging.getLogger('camp13')

        log_cap = StringIO()
        ch = logging.StreamHandler(log_cap)
        ch.setLevel(logging.DEBUG)
        myfmt = logging.Formatter(
            '%(asctime)s - %(name)s: %(message)s')
        ch.setFormatter(myfmt)
        logger.addHandler(ch)

        file = readConfig.get_testFile()
        sheet = readConfig.get_testSheet()
        casesClass = xlsxRead.casesRead(file, sheet)

        Http = configHttp.Http(com.create_CaseName(__name__))
        interfacecase = cominterface1102.interface(Http, log_cap, com.create_CaseName(__name__))

        if casesClass.allCases == None:
            logger.info("重新读excel")
            case = casesClass.get_one_caseNew(7)
        else:
            case = casesClass.get_one_caseNews(17)
        logger.info("用例数据：")
        logger.info(case)

        Http.getauth()

        results = interfacecase.frontapi_exucte(case)

        http_case = runCase1102.runOneCase(case, Http)

        try:
            self.assertTrue(Http.assertResult(http_case["result_http"], case))


        finally:
            results.append(http_case.get("result_lasecase_parm"))
            interfacecase.lastapi_exucte(case, results)

            # testcase = cases.objects.get(id=1)
            # testcase.result_log=log_cap.getvalue()+'\n'
            # testcase.save()




if __name__ == '__main__':
    unittest.main()






















    



    