import logging
logging.basicConfig(level=logging.INFO)
#logging.disable(logging.INFO)
import os
import json
import configparser
config = configparser.RawConfigParser()
# C:\Users\51cto\PycharmProjects\web\mysite\env\Scripts\myweb
# file_config=os.getcwd()+r'\saas\saas_program\config.ini'

#web执行路径
file_config=r'.\saas\saas_program\config.ini'
#单个用例.py执行路径
# file_config=r'.\config.ini'
# print(file_config)
logging.debug(file_config)
config.read(file_config,encoding="utf-8-sig")




# os.environ["environment"]='test'
#test/preLaunch/online
# os.environ["platform"]="前台"
#前台/后台
os.environ['reportEmail']="liaohx@51cto.com"
#测试报告邮件


environment_djangoWeb=''


def get_host():
    os.environ["environment"] = environment_djangoWeb
    if os.environ["environment"] == 'test':
        host = config["headers"]["host"]
    elif os.environ["environment"] == 'preLaunch':
        host = config["headers_preLaunch"]["host"]
    elif os.environ["environment"] == 'online':
        host = config["headers_online"]["host"]

    logging.debug(host)
    return host

# print(get_host())

def get_header():
    if os.environ["environment"] == 'test':
        header = config["headers"]["header"]
    elif os.environ["environment"] == 'preLaunch':
        header = config["headers_preLaunch"]["header"]
    elif os.environ["environment"] == 'online':
        header = config["headers_online"]["header"]
    header = json.loads(header)
    logging.debug(type(header))
    return header


def get_user():
    if os.environ["environment"] == 'test':
        login_param = config["user"]["login_param"]
    elif os.environ["environment"] == 'preLaunch':
        login_param = config["user"]["login_param"]
    elif os.environ["environment"] == 'online':
        login_param = config["user_online"]["login_param"]
    logging.debug(login_param)
    return login_param


def get_testFile():
    # linux
    # return os.path.join(os.getcwd(),r'testFile/测试用例.xlsx')
    # pc web
    return os.path.join(os.getcwd(), r'.\saas\saas_program\testFile\测试用例.xlsx')
    # 单个用例.py
    # return os.path.join(os.getcwd(), r'testFile\测试用例.xlsx')


def get_testSheet():
    # return  config["testCasesFile"]['sheet']
    if os.environ["environment"] == 'test':
        # sheet = 'Sheet2'
        sheet = '测试环境'
    elif os.environ["environment"] == 'preLaunch':
        sheet = '预发环境'
    elif os.environ["environment"] == 'online':
        sheet = '线上环境'
    return sheet


def get_loginSheet():
    return config["testCasesFile"]['loginSheet']


def get_DingDing_url():
    return config["DingDing"]["url"]


def get_emailManage():
    emailMange = {}
    emailMange["host"] = config["Email"]["host"]
    emailMange["port"] = config["Email"]["port"]
    emailMange["account"] = config["Email"]["account"]
    emailMange["password"] = config["Email"]["password"]
    emailMange["sendEmail"] = config["Email"]["sendEmail"]
    # emailMange["acceptEmail"] = config["Email"]["acceptEmail"]
    # emailMange["acceptEmail"]='liaohx@51cto.com'
    emailMange["acceptEmail"] = os.environ['reportEmail']
    return emailMange

def get_testReport():
    '''获取最新的测试报告文件地址'''
    dir=os.path.join(os.getcwd(),r'./saas/saas_program/testFile')
    files=os.listdir(dir)
    files=list(filter(lambda x:x.startswith("Report_email") and x.endswith(".html"),files))
    logging.debug(files)
    files=sorted(files,key=lambda x:os.path.getctime(os.path.join(dir,x)),reverse=True)
    logging.debug(os.path.join(dir, files[0]))
    return os.path.join(dir,files[0])
    # return r'C:\Users\51cto\Desktop\hm_api-master-4b3abf9d035e86f5c28e76ae5294e4bde74cad4f\hm_api-master-4b3abf9d035e86f5c28e76ae5294e4bde74cad4f\hm\testFile\Report_email2021-08-11-18_41_10.html'


def get_testReport_log():
    '''获取最新的测试报告(有log)文件地址'''
    dir=os.path.join(os.getcwd(),r'templates')
    files=os.listdir(dir)
    files=list(filter(lambda x:x.startswith("Report_log") and x.endswith(".html"),files))
    logging.debug(files)
    files=sorted(files,key=lambda x:os.path.getctime(os.path.join(dir,x)),reverse=True)
    logging.debug(os.path.join(dir, files[0]))
    return os.path.join(dir,files[0])

def get_db():
    db={}
    db["host"]=config["DB"]["host"]
    db["account"] = config["DB"]["account"]
    db["password"] = config["DB"]["password"]
    db["database"] = config["DB"]["database"]
    return db

def get_redis():
    redis={}
    redis["host"] = config["redis"]["host"]
    redis["port"] = config["redis"]["port"]
    redis["password"] = config["redis"]["password"]
    return redis


def get_mongoDB():
    mongoDB={}
    mongoDB["host"] = config["mongoDB"]["host"]
    mongoDB["port"] = config["mongoDB"]["port"]
    mongoDB["user"] = config["mongoDB"]["user"]
    mongoDB["password"] = config["mongoDB"]["password"]
    mongoDB["dbname"] = config["mongoDB"]["dbname"]
    return mongoDB









