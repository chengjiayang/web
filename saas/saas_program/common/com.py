import re
import time
import random
import logging
from hashlib import md5
from time import time
from  datetime import datetime
import functools
import requests
logging.basicConfig(level=logging.INFO)

def find(keyz,dicts):
    '''循环遍历接口返回值中是否包含某键值'''
    zdl=False

    def excute(keyz,dicts):
        nonlocal zdl
        if not zdl:
            for k, v in dicts.items():
                if k == keyz:
                  zdl=True
                if type(v) ==dict:
                  excute(keyz, v)
                if type(v)==list:
                    for v1 in v:
                        if type(v1) == dict:
                            excute(keyz, v1)
    if type(dicts)==dict:
        excute(keyz,dicts)

    return zdl

#待优化
def getValue1(keyz,dicts):
    zdl = None

    def excute(keyz, dicts):
        nonlocal zdl
        if not zdl:
            for k, v in dicts.items():
                if k == keyz:
                    zdl = v
                if type(v) == dict:
                    excute(keyz, v)
                if type(v) == list:
                    for v1 in v:
                        if type(v1) == dict:
                            excute(keyz, v1)

    if type(dicts) == dict:
        excute(keyz, dicts)

    return zdl

def getValue(keyz,dicts):
    zdl = []
    # logging.info(keyz)
    # logging.info(dicts)

    def excute(keyz, dicts):
        nonlocal zdl
        for k, v in dicts.items():
            if k == keyz:
                zdl.append(v)
            if type(v) == dict:
                excute(keyz, v)
            if type(v) == list:
                for v1 in v:
                    if type(v1) == dict:
                        excute(keyz, v1)


    if type(dicts) == dict:
        excute(keyz, dicts)

    if len(zdl)==0:
        return None
    else:
        # return zdl[-1]
        return zdl[0]

def unique():
    '''创建唯一值，避免重复参数'''
    # return str(int(time.time()*1000000))
    return ''.join(random.sample("qwertyuiopasdfghjklzxcvbnm0123456789",10))

def get_time():
    '''获取当前时间戳，保留三位微秒'''
    # return round(time() * 1000)
    return round(time())
def get_now():
    '''获取当前时间，2021-05-20 10:53:00格式'''
    return datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
#harmony接口验签
def sign(method,timenow,token):
    '''生成接口验签'''
    # time_now = round(time() * 1000)
    def bian(x):
        m = md5()
        m.update(x.encode("utf-8"))
        return m.hexdigest()

    sign=bian(bian(method+str(timenow)+str(bian(token))))
    # logging.info(bian(token))
    # logging.info(method+str(timenow)+str(bian(token)))
    # logging.info(bian(method + str(timenow) + str(bian(token))))
    # logging.info(sign)
    return sign


def textTojson(l):
    ''' text/html请求参数转json'''
    # logging.info("textTojson函数入参：%s"%str(l))
    # logging.info("textTojson函数入参类型：%s" % str(type(l)))
    # l=str(l)
    if '=' in l:
        l = l.split('&')
        logging.debug(l)
        s = {}
        for i in l:
            key = i.split('=')[0]
            value = i.split('=')[1]
            s[key] = value
        # if 'sign'in s.keys():
        #     s.pop("sign")
        # if 'timestamp' in s.keys():
        #     s.pop("timestamp")
        # if 'token' in s.keys():
        #     s.pop("token")
        return s
    else:
        return l



def jsonTotext(s):
    '''json请求参数转text/html'''

    m=[]
    for key, value in s.items():
        i = str(key) + '=' + str(value)
        m.append(i)
    m = '&'.join(m)
    return m




def create_CaseName(ClassName):
    '''test_articles_articlesType 处理成articles_articlesType'''
    # a = ClassName.lstrip("test_")
    a=ClassName[5:]
    # print(a)
    return a



def run_times(time=2):

    def runx(f):
        @functools.wraps(f)
        def runy(*args,**kwargs):
            time_excute = 0
            while time_excute < time:
                try:
                    f(*args, **kwargs)
                    time_excute = time
                except:
                    time_excute = time_excute + 1
                    if time_excute == time:
                        raise




        return runy
    return runx





# print(textTojson("method=specialissue.edit&title=%E9%B8%BF%E8%92%99%E6%8A%80%E6%9C%AF%E7%89%B9%E5%88%8A%20NO.X%E6%9C%9F&issue_num=NO.X%E6%9C%9F&cover=images%2F202103%2F67b4e72799756622071731a859209ce10e1bc4.jpeg&top_title=test1&top_cover=images%2F202103%2F96a00d2252d39e1d9048190415fae934380eb4.png&top_uid=0&top_url=http%3A%2F%2Fweb.hmtest.51cto.com%2Fposts%2F3028&content=%5B%7B%22source_id%22%3A%223028%22%2C%22sort%22%3A1%2C%22type%22%3A1%7D%5D&activity_id=&id=80&share_image=images%2F202104%2F78a108241afae4fe3045384b9248b36d3aaa0f.jpg&sign=a1ccd138e2df6c73ced81a7b99ea6f33&timestamp=1617274002346&token=21d8CAFSAAVUBFZXVQAGBQQLVFJVUA4OUgFSV1gLWAJQB1JdDw&user_token=87aaAg8CBwwGAlADAlQEBgIAVVAHXVVfBQIAU1lxQ316cFt9YHhZd1JuFGRRRAkMQ1pSaHoMAz5FCgsNcw8EWFg&login_user_id=13648560"))

# print(get_now())


















