import os
import logging
import time

logging.basicConfig(level=logging.INFO)


# logging.disable(logging.INFO)
def create(case,login_data,environment,count=1):
    description = case["information"] + ':' + case["name"]
    if '.'in case["name"]:
        case["name"]=case["name"].replace('.','_')
    file_path = os.path.join(os.getcwd(), r'saas\saas_program\testCase')
    file_name = os.path.join(file_path, 'test_%s.py' % (case['name']+str(int(time.time()))))
    logging.debug(file_name)
    file_case = open(file_name, 'w', encoding='utf-8')

    logging.debug(description)

    content = '''
    

import logging  
from saas.saas_program import readConfig  
import unittest
from saas.saas_program.common import xlsxRead,configHttp,runCase1102,com,cominterface1202,mywebDB
from io import StringIO


from ddt import data,ddt
logging.basicConfig(level=logging.INFO)



len=list(range(0,{count}))
@ddt
class TestCase{classname}(unittest.TestCase):
    @data(*len)
    
   
    def test_{testname}(self,a):
        '{information}'
        logger =logging.getLogger(com.create_CaseName(__name__))
        
        log_cap = StringIO()
        ch = logging.StreamHandler(log_cap)
        ch.setLevel(logging.DEBUG)
        myfmt = logging.Formatter(
            '%(asctime)s - %(name)s: %(message)s')
        ch.setFormatter(myfmt)
        logger.addHandler(ch)
        
        
       
        Http = configHttp.Http('{environment}',com.create_CaseName(__name__))
        interface=cominterface1202.interface(Http,log_cap,com.create_CaseName(__name__))
        
       
        case={case}
        logger.info("用例数据：")
        logger.info(case)
        
        
        Http.getauth({login_data})
       
        
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


    



     ''' .format (classname=case["name"],testname=case["name"],  information=description,logname=case["name"],case=case,login_data=login_data,environment=environment,count=count)
    file_case.write(content)

    file_case.close()

    return file_name










