import chardet
import json
import re
import logging
logging.basicConfig(level=logging.INFO)
# logging.disable(logging.INFO)


# def hostselect(url,hosts):
#     result = False
#     for host in hosts:
#         if url.startswith(host):
#             result=True
#             break
#     return result

# hostselect()

def getDatas(hosts):
    '''从fiddler录制的接口文件中取接口数据'''
    # hosts=[
    # "http://api.hmtest.51cto.com",
    # "http://backend.bhmtest.51cto.com"
    # "https://saas-test-api.51cto.com"
    # 'https://glbsit-cms-dev-bus.starvisioncloud.com'
    # 'https://glbsit-wuhan-custom.starvisioncloud.com'
    # ]

    resultDatas=[]
    with open(r'D:\auto.dat', 'rb') as f1:
        list1 = f1.read()
        result = chardet.detect(list1)
        list1 = list1.decode(encoding=result['encoding'])
    list1 = list1.splitlines(False)
    # logging.info(list1)
    # logging.info(list1[0])
    logging.info(list1[1] == '')
    # logging.info(list1[3])
    print(len(list1))
    datas = []
    for list_1 in list1:
        if list_1 != '':
            list_1 = json.loads(list_1)
            datas.append(list_1)
    print(len(datas))



    def host_get(case):
        result=False
        for host in hosts:
            if case["url"].startswith(host):
                result=True

        return  result


    # datas = list(filter(lambda x: x["url"].startswith(host), datas))
    datas =list(filter(host_get, datas))
    datas = list(filter(lambda x: x["request_method"] in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE'), datas))
    # datas = list(filter(lambda x: str(x["response_code"]).startswith('2'), datas))
    # datas=filter(lambda x:x!='',datas)
    print(len(datas))
    for data in datas:
        for hosta in hosts:
            if data['url'].startswith(hosta):
                host=hosta
        data["host"]=host
        data['url'] = data['url'].split(host)[1]
        urls = data['url'].split('?')
        data["url"] = urls[0]
        if len(urls) == 2:
            data['url_params'] = urls[1]
        else:
            data['url_params'] = None


        resultDatas.append(data)
    resultDatas1=[]
    for data in resultDatas:
        data["url_params"] = datacode(data["url_params"])
        # data["url_params"] =data["url_params"]
        data["request_body"] = datacode(data["request_body"])
        # data["request_body"]=data["request_body"]
        resultDatas1.append(data)
    # resultDatas2 = []
    # for data in resultDatas1:
    #     valueName = get_m(data)
    #     data["m"] = valueName
    #     resultDatas2.append(data)
    #
    #
    #    # print(data)
    #
    # resultDatas3 = []
    # for data in resultDatas2:
    #     valueName = get_do(data)
    #
    #     data["do"] = valueName
    #     resultDatas3.append(data)

    return resultDatas1


#

#saas接口处理，勿删
def quchonga(resultDatas):
    '''saas接口去重'''
    print('去重前' + str(len(resultDatas)))
    list1=[]
    resultDatas1=[]
    for data in resultDatas:
        valueHost=data["host"]
        valueUrl=data["url"]
        valueUrl=clearNumericData(valueUrl)
        valueUrl_params = data["url_params"]
        valueRequest_body = data["request_body"]
        valueMethod = data["request_method"]
        # valuem=data["m"]
        # valuedo=data["do"]
        # valueMethod=data["request_method"]


        # values=(valueUrl,valueUrl_params,valueRequest_body,valueMethod)
        values = (valueUrl,valueMethod)
        # values=(valueUrl,valuem,valuedo,valueMethod)
        if values not in list1:
            list1.append(values)
            resultDatas1.append(data)

    print('去重后' + str(len(resultDatas1)))
    # print(resultDatas1)
    return resultDatas1

def quchong(resultDatas):
    '''鸿蒙接口去重'''
    print('去重前' + str(len(resultDatas)))
    list1=[]
    resultDatas1=[]
    for data in resultDatas:
        valueUrl=data["url"]

        valueType=data["request_method"]
        # valueName=data["name"]
        method=get_method(data)




        # values=(valueUrl,valueType,valueName)
        values = (valueUrl, valueType, method)
        if values not in list1:
            list1.append(values)
            resultDatas1.append(data)

    print('去重后' + str(len(resultDatas1)))
    # print(resultDatas1)
    return resultDatas1


def get_method(data):
    '''鸿蒙接口从入参中取method值'''
    method = None
    if data["url_params"]!=None:
        if 'method' in data["url_params"]:
            # print(data["url_params"])
            # a=re.match('method=([a-zA-Z.0-9])+', data["url_params"])
            # print(a)
            s = re.compile("method=[a-zA-Z.0-9_]+")
            a=s.search(data["url_params"])
            if a!=None:
               method=a.group().split('=')[1]
    if data["request_body"] != None:
        if 'method' in data["request_body"]:
            # print(data["request_body"])
            # a = re.match('method=([a-zA-Z.0-9])+', data["request_body"])
            # print(a)
            s = re.compile("method=[a-zA-Z.0-9_]+")
            a = s.search(data["request_body"])
            if a!=None:
               method=a.group().split('=')[1]
    return method

def get_m(data):
    '''学院APP接口，从入参中取m值'''
    m = None
    if data["url_params"]!=None:
        if 'm' in data["url_params"]:
            # print(data["url_params"])
            # a=re.match('method=([a-zA-Z.0-9])+', data["url_params"])
            # print(a)
            s = re.compile("m=[a-zA-Z.0-9_]+")
            a=s.search(data["url_params"])
            if a!=None:
               m=a.group().split('=')[1]
    if data["request_body"] != None:
        if 'm' in data["request_body"]:
            # print(data["request_body"])
            # a = re.match('method=([a-zA-Z.0-9])+', data["request_body"])
            # print(a)
            s = re.compile("m=[a-zA-Z.0-9_]+")
            a = s.search(data["request_body"])
            if a!=None:
               m=a.group().split('=')[1]
    return m

def get_do(data):
    '''学院APP接口，从入参中取do值'''
    do = None
    if data["url_params"]!=None:
        if 'do' in data["url_params"]:
            # print(data["url_params"])
            # a=re.match('method=([a-zA-Z.0-9])+', data["url_params"])
            # print(a)
            s = re.compile("do=[a-zA-Z.0-9_]+")
            a=s.search(data["url_params"])
            if a!=None:
               do=a.group().split('=')[1]
    if data["request_body"] != None:
        if 'do' in data["request_body"]:
            # print(data["request_body"])
            # a = re.match('method=([a-zA-Z.0-9])+', data["request_body"])
            # print(a)
            s = re.compile("do=[a-zA-Z.0-9_]+")
            a = s.search(data["request_body"])
            if a!=None:
               do=a.group().split('=')[1]
    return do
# s=re.compile("method=[a-zA-Z.0-9]+")
# print(s.search("content=234444&").group())
def datacode(l):
    '''字段处理：去除ver,time,sign,devices,deviceNumber,channel'''
    #
    # sign, timestamp, token, user_token, login_user_id
    try:
        if l != None:
            if '&' in l:
                l = l.split('&')
                # print(l)
                s = {}
                for i in l:
                    key = i.split('=')[0]
                    value = i.split('=')[1]
                    s[key] = value
                if 'ver' in s.keys():
                    s.pop("ver")
                if 'time' in s.keys():
                    s.pop("time")
                if 'sign' in s.keys():
                    s.pop("sign")
                if 'devices' in s.keys():
                    s.pop("devices")
                if 'deviceNumber' in s.keys():
                    s.pop("deviceNumber")
                if 'channel' in s.keys():
                    s.pop("channel")
                if 'timestamp' in s.keys():
                    s.pop("timestamp")
                if 'token' in s.keys():
                    s.pop("token")
                if 'user_token' in s.keys():
                    s.pop("user_token")
                if 'login_user_id' in s.keys():
                    s.pop("login_user_id")
                m = []
                for key, value in s.items():
                    i = key + '=' + value
                    m.append(i)
                m = '&'.join(m)
                l = m
    except:
        l=l

    #fiddler 抓包日志中请求body为字符串类型,需转换成dict
    if type(l)==str:
        try:
            l=json.loads(l)
        except:
            l=l


    return l


def clearNumericData(m):
    #去除url中数据,以不同数据的同一个请求筛选
    #'shakespeare/notes/108710063/included_collections'转换成'shakespeare/notes//included_collections'
    m = m.split('/')
    x = []
    print(m)
    for a in m:
        if bool(re.search(r'\d', a)):
        #包含数字
        # if a.isnumeric():
            #纯数字
            m[m.index(a)] = ''

    m = '/'.join(m)
    return m










































# dict_list = [{'a': 1, 'b': 2, 'c': 1}, {'a': 1, 'b': 2, 'c': 8}, {'a': 1, 'b': 2, 'c': 2}, {'a': 3, 'b': 5, 'c': 8}]
# d_list = []
# dict_list2 = []
# for dict_item in dict_list:
#     val_a = dict_item['a']
#     val_b = dict_item['b']
#     new_tuple = (val_a, val_b,)
#     if new_tuple not in d_list:
#         d_list.append(new_tuple)
#         dict_list2.append(dict_item)
#     else:
#         print('被移除元素：', dict_item)
#
# print(dict_list2)