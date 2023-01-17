
    

import logging  
from saas.saas_program import readConfig  
import unittest
from saas.saas_program.common import xlsxRead,configHttp,runCase1102,com,cominterface1202,mywebDB
from io import StringIO


from ddt import data,ddt
logging.basicConfig(level=logging.INFO)



len=list(range(0,1))
@ddt
class TestCase549(unittest.TestCase):
    @data(*len)
    
   
    def test_549(self,a):
        '学员考试任务提交接口-考生查询自己某场考试的试卷信息-及当前已答过的答案信息-开始答题-考试进行中查看（已开始答题）:549'
        logger =logging.getLogger(com.create_CaseName(__name__))
        
        log_cap = StringIO()
        ch = logging.StreamHandler(log_cap)
        ch.setLevel(logging.DEBUG)
        myfmt = logging.Formatter(
            '%(asctime)s - %(name)s: %(message)s')
        ch.setFormatter(myfmt)
        logger.addHandler(ch)
        
        
       
        Http = configHttp.Http('test',com.create_CaseName(__name__))
        interface=cominterface1202.interface(Http,log_cap,com.create_CaseName(__name__))
        
       
        case={'id': 549, 'project': None, 'name': '549', 'url': '/exam/exams/tasks/{id}/questions', 'method': 'GET', 'url_params': 'id={mongoDB:id}&solutionId={solutionId}', 'body_params': '', 'file': None, 'code': 200, 'unchange': '', 'change': 'id', 'information': '学员考试任务提交接口-考生查询自己某场考试的试卷信息-及当前已答过的答案信息-开始答题-考试进行中查看（已开始答题）', 'result_log': None, 'is_online': '否'}
        logger.info("用例数据：")
        logger.info(case)
        
        
        Http.getauth({'username': 'liaohx1@51cto.com', 'password': '88888888', 'type': 'password'})
       
        
        results=interface.frontapi_exucte(case)

        http_case = runCase1102.runOneCase(case,Http)

        try:
            self.assertTrue(Http.assertResult(http_case["result_http"], case))
        finally:
            results.append(http_case.get("result_lasecase_parm"))
            
            interface.lastapi_exucte(case,results)
            
            
            result_log=log_cap.getvalue()
            
            
        



if __name__ == '__main__':
    unittest.main()


    



     