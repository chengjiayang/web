import celery
from django.shortcuts import render,HttpResponse,redirect
from saas.models import *
# Create your views here.
from django import forms
import unittest
import datetime
from saas.saas_program import run_web
from saas.saas_program.common import mywebDB,creatCaseFile1102,zipCreate
from django.forms.models import model_to_dict
import time
from dwebsocket.decorators import accept_websocket,require_websocket
from myweb import settings
from saas.tasks import add
from .models import casenew
from celery.result import AsyncResult
import  os
from django.http import StreamingHttpResponse
from django.views import View
import json
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from saas.serializer import *
from saas.pagination import *
from django.db.models import Q
import os
from saas import  fiddlerExe
from rest_framework import viewsets

def test(request):
    basecase=casenew.objects.filter(id=4)
    # relatecase=basecase.related.all()

    # result=model_to_dict(relatecase[0])
    # print(result)
    # print(type(result))
    # relation=relationship.objects.filter(status=True,basecase=basecase)
    # relation = model_to_dict(relation[1])
    # print(relation)
    # case1=mywebDB.lgetCasebyId(casenew,4)
    # print(case1)
    # case2=mywebDB.getCasebyId(casenew,5)
    relationship.objects.filter(status=True,basecase=basecase,type=0)

    return HttpResponse('ok')

def runtest(request):
    case_path = r'.\saas\saas_program'

    # 第一个参数，文件路径，第二个参数，匹配规则，如果本来就是以test开头的，则可不传
    suite = unittest.defaultTestLoader.discover(case_path, 'test*.py')
    unittest.TextTestRunner().run(suite)


    # return render(request,"result_case.html",{"result":cases.objects.get(id=1).result_log})
    # return render(request, "result_case.html", {"result": result})
    return HttpResponse("OK")




def gettime(request):
    context={}
    context["time"]=datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
    return render(request,"test.html",context)
    # return HttpResponse(datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S"))

def data_excute(request):
    data=cases(name='camp')

    data.save()
    return HttpResponse(data.name)




class LoginForm(forms.Form):
    username = forms.CharField(min_length=8, label="用户名")
    pwd = forms.CharField(min_length=6, label="密码")


def ParentTemplate(request):

    return render(request, "ParentTemplate.html")


def SunTemplate(request):
    return render(request, "SunTemplate.html")

# def index(request):
#     return render(request, 'change_list.html')


def project(request):
     projects = Project.objects.all().order_by("-id") # 使用负id是为了倒序取出项目数据
     # return HttpResponse(projects[0].name)
     # print(projects)
     return render(request, 'project.html', {'projects': projects})

def case(request):
    if request.method=='GET':
        cases_list=cases.objects.all().order_by("-id")
        # cases_list_new=[]
        # for case in cases_list:
        #     case=model_to_dict(case)
        #     for key,value in case.items():
        #         if value==None:
        #             case[key]=''
        #     cases_list_new.append(case)

        return render(request, 'case_list.html',{"caseslist":cases_list})
    else:
        # cases.objects.create(name=request.POST["name"],
        #                      url=request.POST["url"],
        #                      method=request.POST["method"],
        #                      url_params=request.POST["url_params"],
        #                      body_params=request.POST["body_params"],
        #                      file=request.POST["file"],
        #                      code=request.POST["code"],
        #                      unchange=request.POST["unchange"],
        #                      information=request.POST["information"]
        #                      )
        # caseList=[]
        files = []
        for id in request.POST.getlist("caseId_selected"):
            print(id)
            case=mywebDB.getCasebyId(cases,id)
            files.append(creatCaseFile1102.create(case))
        run_web.runallcases(files)
        # print(request.POST["caseId_selected"])
        return redirect('/result')
        # return redirect('/logs')


def result(request):

    return  render(request,"Report_log.html")

def result_one_thread(request):
    return  render(request,"Result_log.html")

#time.ctime(
def result_last(request):
    result_log_time=os.stat(r"./templates/Result_log.html").st_mtime
    report_log_time = os.stat(r"./templates/Report_log.html").st_mtime
    print(result_log_time)
    print(report_log_time)
    if result_log_time> report_log_time:
        return render(request,"Result_log.html")
    else:
        return render(request, "Report_log.html")

# @accept_websocket
def logs(request):
    # if request.is_websocket():
    #     message = request.websocket.wait()
    #     request.websocket.send(message)
    # else:
    # task_id=request.GET.get("task_id")
    # print(task_id)

    # ta=AsyncResult(task_id)
    # if ta.ready():
    #     print(ta.status)
    return render(request,'logs.html')

        #settings.LOG_FILE
        # with open(r'./logs/all-2021-12-09.log', 'r', encoding='UTF-8') as f:
        #     log_length = len(f.readlines())
        #     time.sleep(1)
        # while True:
        #     with open(r'./logs/all-2021-12-09.log', 'r', encoding='UTF-8') as f:
        #         contents = f.readlines()
        #         length_tmp = len(contents)
        #     for i in range(log_length, length_tmp):
        #         request.websocket.send(contents[i].encode('utf-8'))
        #     log_length = length_tmp
        #     time.sleep(1)
    # else:
    #     return render(request, 'logs.html')

def logs_one_thread(request):

    return render(request,'logs_one_thread.html')
def logsx(request):
    return render(request,'logs.html')


def post(request):
    result = add.delay(2, 3)


import logging
# def httest(request):
#     add.delay(0,1)
#     # for i in range(10):
#     #     logging.info(i)
#     #     time.sleep(i)
#     return render(request, 'change_list.html')




def download(request):
    files=os.listdir(r'./saas/saas_program/testFile/DownloadFiles')
    file_count=len(files)
    if file_count==0:
        return HttpResponse("没有下载文件")
    elif file_count==1:
        filea=files[0]
        file = os.path.join(r'./saas/saas_program/testFile/DownloadFiles', filea)
        file_content = open(file, 'rb')
        response = HttpResponse(file_content)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{name}"'.format(name=filea).encode('utf-8','ISO-8859-1')
        return response
    elif file_count>1:
        utilities = zipCreate.ZipUtilities()
        for filea in os.listdir(r'./saas/saas_program/testFile/DownloadFiles'):
            file = os.path.join(r'./saas/saas_program/testFile/DownloadFiles', filea)
            utilities.toZip(file, filea)
        response = StreamingHttpResponse(utilities.zip_file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{name}"'.format(name='下载文件合集.zip').encode('utf-8',
                                                                                                          'ISO-8859-1')
        return response









    # if request.method == 'POST':
        # 判断文件存不存在




    # for filea in os.listdir(r'./saas/saas_program/testFile/DownloadFiles'):
    #     response=None
    #     file = os.path.join(r'./saas/saas_program/testFile/DownloadFiles', filea)
    #     file_content = open(file, 'rb')
    #     response = HttpResponse(file_content)
        # 告诉response返回的是文件

    # response['Content-Type'] = 'application/zip'
    # response['Content-Disposition'] = 'attachment;filename="{name}"'.format(name='mod_result.zip').encode('utf-8',
    #                                                                                                       'ISO-8859-1')

class projectList(GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    search_fields = ['name', 'leader','nameEng']
    pagination_class = PageNumberPagination
    def post(self,request):
        '''新增'''
        # datas = json.loads(request.body.decode('utf-8'))
        # serialize = self.get_serializer(data=datas)
        serialize = self.get_serializer(data=request.data)
        try:
            serialize.is_valid(raise_exception=True)
        except:
            return Response(serialize.errors)
        serialize.save()
        return Response(serialize.data)

    def get(self,request):
        '''查询'''
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)




    # def get(self, request, pk):
    #
    #     '''列表，详情，条件查询'''
    #     pro=None
    #     if projectId!=None:
    #         pro=Project.objects.filter(id=projectId)
    #     elif  request.GET.get("name" ,None):
    #         pro=Project.objects.filter(name__contains=request.GET['name'])
    #     else:
    #         pro=Project.objects.all()
    #
    #     pro_result=[]
    #     if pro!=None:
    #
    #         pro_v={}
    #         for pro_a in pro:
    #
    #             pro_v={'name':pro_a.name}
    #             pro_result.append(pro_v)
    #
    #     return HttpResponse(
    #         json.dumps({"msg": "success", "data": pro_result,'total':len(pro_result)}, ensure_ascii=False),
    #         content_type="application/json,charset=utf-8"
    #     )
    #
    # def post(self, request):
    #     '''新增，修改'''
    #
    #     pass
    #
    # def delete(self, request):
    #     '''删除'''
    #     pass
class projectInfo(GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    def get(self, request, pk):
        '''详情'''
        pro=self.get_object()
        return Response(self.get_serializer(pro).data)


    def put(self, request, pk):
        '''修改'''
        # pro = self.get_object()
        # datas=request.data
        # serialize=self.get_serializer(data=datas, partial=True)
        project = Project.objects.get(id=pk)
        serialize= ProjectModelSerializer(project,data=request.data, partial=True)

        # try:
        #     serialize.is_valid(raise_exception=True)
        # except:
        #     return Response(serialize.errors)
        # pro.name= serialize.validated_data['name']
        # pro.nameEng= serialize.validated_data['nameEng']
        # pro.leader = serialize.validated_data['leader']
        # pro.save()
        # return Response(serialize.data)

        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        else:
            return Response(serialize.errors)


    def delete(self, request,pk):
        '''删除'''
        pro = self.get_object()
        pro.delete()
        return Response(dict(self.get_serializer(pro).data,**{"msg":'删除成功'}))


class moduleList(GenericAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleModelSerializer
    search_fields = ['name', 'nameEng','project__name','project__nameEng']
    pagination_class = PageNumberPagination
    def post(self,request):
        '''新增'''
        # datas = json.loads(request.body.decode('utf-8'))
        serialize = self.get_serializer(data=request.data)
        try:
            serialize.is_valid(raise_exception=True)
        except:
            return Response(serialize.errors)
        serialize.save()
        return Response(serialize.data)

    def get(self,request):
        '''查询'''
        if request.GET.get('project',None):
            query=self.get_queryset().filter(project=request.GET['project'])
        else:
            query = self.get_queryset()
        queryset = self.filter_queryset(query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            mods=[]
            for mod in serializer.data:
                if mod['project']!=None:
                    pro=Project.objects.get(id=mod['project'])
                    mod['project']=pro.name
                else:
                    mod['project'] = ''
                mods.append(mod)
            return self.get_paginated_response(mods)

        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)

class moduleInfo(GenericAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleModelSerializer
    def get(self, request, pk):
        '''详情'''
        pro=self.get_object()
        return Response(self.get_serializer(pro).data)


    def put(self, request, pk):
        '''修改'''
        # mod = self.get_object()
        # datas = request.data
        # serialize=self.get_serializer(data=datas)
        # try:
        #     serialize.is_valid(raise_exception=True)
        # except:
        #     return Response(serialize.errors)
        # mod.name= serialize.validated_data['name']
        # mod.nameEng = serialize.validated_data['nameEng']
        # mod.project = serialize.validated_data['project']
        # mod.save()
        # return Response(serialize.data)

        module = Module.objects.get(id=pk)
        serialize = ModuleModelSerializer(module, data=request.data, partial=True)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        else:
            return Response(serialize.errors)


    def delete(self, request,pk):
        '''删除'''
        pro = self.get_object()
        pro.delete()
        return Response(dict(self.get_serializer(pro).data,**{"msg":'删除成功'}))


class caseList(GenericAPIView):
    queryset = casenew.objects.all()
    serializer_class = CaseModelSerializer
    search_fields = ['id', 'url','information', 'project__name', 'project__nameEng',
                     'module__name', 'module__nameEng', ]
    pagination_class = PageNumberPagination

    def post(self, request):
        '''新增'''
        # datas = json.loads(request.body.decode('utf-8'))
        datas=request.data
        relateds=datas['related']
        datas.pop('related')
        serialize = self.get_serializer(data=datas)
        try:
            serialize.is_valid(raise_exception=True)
        except:
            return Response(serialize.errors)

        serialize.save()
        for relate in relateds:
            if relate["relatedcase"] or relate["interfaceProcess"] or relate["sqls"] or relate["m_table"] or relate["interfaceRequest_url"] or relate["interfaceRequest_body"] :
                datas2 = dict(relate, **{'basecase': serialize.data['id']})
                serialize2 = RelationshipModelSerializer(data=datas2)
                try:
                    serialize2.is_valid(raise_exception=True)
                except:
                    return Response(serialize2.errors)
                serialize2.save()




        return Response(serialize.data)

    def get(self, request):
        '''查询'''
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            cases = []
            for case in serializer.data:
                # case["method"] = self.get_serializer(data=case).get_method_display()
                if case['project'] != None:
                    pro = Project.objects.get(id=case['project'])
                    case['project'] = pro.name
                else:
                    case['project'] = ''

                if case['module'] != None:
                    mod = Module.objects.get(id=case['module'])
                    case['module'] = mod.name
                else:
                    case['module'] = ''

                if case['is_online']:
                    case['is_online']='是'
                else:
                    case['is_online'] = '否'

                if case['formal_case']:
                    case['formal_case']='是'
                else:
                    case['formal_case'] = '否'

                # if case['related'] != None:
                #     case_relate = casenew.objects.get(id=case['related'].id)
                #     case['related'] = case_relate.information
                # else:
                #     case['related'] = ''
                cases.append(case)
            return self.get_paginated_response(cases)

        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)



class caseInfo(GenericAPIView):
    queryset = casenew.objects.all()
    serializer_class = CaseModelSerializer

    def get(self, request, pk):
        '''详情'''
        pro = self.get_object()
        return Response(self.get_serializer(pro).data)

        # '''列表，详情，条件查询'''
        # pro=None
        # if projectId!=None:
        #     pro=Project.objects.filter(id=projectId)
        # elif  request.GET.get("name" ,None):
        #     pro=Project.objects.filter(name__contains=request.GET['name'])
        # else:
        #     pro=Project.objects.all()
        #
        # pro_result=[]
        # if pro!=None:
        #
        #     pro_v={}
        #     for pro_a in pro:
        #
        #         pro_v={'name':pro_a.name}
        #         pro_result.append(pro_v)
        #
        # return HttpResponse(
        #     json.dumps({"msg": "success", "data": pro_result,'total':len(pro_result)}, ensure_ascii=False),
        #     content_type="application/json,charset=utf-8"
        # )

    def put(self, request, pk):
        '''修改'''
        mod = self.get_object()
        datas = request.data

        serialize = self.get_serializer(data=datas)
        relateds = datas['related']
        datas.pop('related')

        try:
            serialize.is_valid(raise_exception=True)
        except:
            return Response(serialize.errors)
        mod.project = serialize.validated_data['project']
        mod.module = serialize.validated_data['module']
        mod.url = serialize.validated_data['url']
        mod.method = serialize.validated_data['method']
        mod.url_params = serialize.validated_data['url_params']
        mod.body_params = serialize.validated_data['body_params']
        mod.file = serialize.validated_data['file']
        mod.code = serialize.validated_data['code']
        mod.unchange = serialize.validated_data['unchange']
        mod.change = serialize.validated_data['change']
        mod.information = serialize.validated_data['information']
        mod.is_online = serialize.validated_data['is_online']
        mod.formal_case=serialize.validated_data['formal_case']
        mod.save()

        relation_current=relationship.objects.filter(basecase=mod.id)
        [x.delete() for x in relation_current]
        if relateds!=[]:
            for relate in relateds:
                if relate["relatedcase"] or relate["interfaceProcess"] or relate["sqls"] or relate["m_table"] or relate[
                    "interfaceRequest_url"] or relate["interfaceRequest_body"]:
                    datas2 = dict(relate, **{'basecase': pk})
                    serialize2 = RelationshipModelSerializer(data=datas2)
                    try:
                        serialize2.is_valid(raise_exception=True)
                    except:
                        return Response(serialize2.errors)

                    serialize2.save()




        return Response(serialize.data)

    def patch(self, request, pk):
        '''修改'''
        mod = self.get_object()
        datas = request.data

        serialize = self.get_serializer(mod,data=datas,partial=True)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        else:
            return Response(serialize.errors)

    def delete(self, request, pk):
        '''删除'''
        pro = self.get_object()
        pro.delete()
        return Response({'id':pk,"msg": '删除成功'})



# class relationList()
class relationList(GenericAPIView):
    queryset = relationship.objects.all()
    serializer_class = RelationshipModelSerializer
    search_fields = [ 'basecase__information', 'relatedcase__information']
    pagination_class = PageNumberPagination

    def post(self, request):
        '''新增'''
        # datas = json.loads(request.body.decode('utf-8'))
        serialize = self.get_serializer(data=request.data)
        try:
            serialize.is_valid(raise_exception=True)
        except:
            return Response(serialize.errors)
        serialize.save()
        return Response(serialize.data)

    def get(self, request):
        '''查询'''
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            # mods = []
            # for mod in serializer.data:
            #     base = casenew.objects.get(id=mod['basecase'])
            #     mod['basecase'] = base.information
            #     related = casenew.objects.get(id=mod['relatedcase'])
            #     mod['relatedcase'] = base.information
            #     mods.append(mod)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)


class relationInfo(GenericAPIView):
    queryset = relationship.objects.all()
    serializer_class = RelationshipModelSerializer

    def get(self, request, pk):
        '''详情'''
        pro = self.get_object()
        # base = casenew.objects.get(id=mod['basecase'])
        # mod['basecase'] = base.information
        # related = casenew.objects.get(id=mod['relatedcase'])
        # mod['relatedcase'] = base.information

        return Response(self.get_serializer(pro).data)

    def put(self, request, pk):
        '''修改'''
        mod = self.get_object()
        # datas=json.loads(request.body.decode('utf-8'))
        datas = request.data
        serialize = self.get_serializer(data=datas)
        try:
            serialize.is_valid(raise_exception=True)
        except:
            return Response(serialize.errors)
        mod.basecase = serialize.validated_data['basecase']
        mod.relatedcase = serialize.validated_data['relatedcase']
        mod.interfaceProcess = serialize.validated_data['interfaceProcess']
        mod.sqls = serialize.validated_data['sqls']
        mod.m_table = serialize.validated_data['m_table']
        mod.m_query = serialize.validated_data['m_query']
        mod.m_order = serialize.validated_data['m_order']
        mod.m_result = serialize.validated_data['m_result']
        mod.interfaceRequest_url = serialize.validated_data['interfaceRequest_url']
        mod.interfaceRequest_body = serialize.validated_data['interfaceRequest_body']
        mod.save()
        return Response(serialize.data)

    def delete(self, request, pk):
        '''删除'''
        pro = self.get_object()
        pro.delete()
        return Response(dict(self.get_serializer(pro).data, **{"msg": '删除成功'}))


def deleteAuto(request):

    if os.path.exists(r"D:\auto.dat"):
        os.remove(r"D:\auto.dat")
    # return HttpResponse({"results":'删除fiddler日志文件成功'})
    return HttpResponse(
            json.dumps({"results":'删除fiddler日志文件成功'}, ensure_ascii=False),
            content_type="application/json,charset=utf-8"
        )

class dealFiddlerOnly(GenericAPIView):
    def post(self,request):
        '''body传参{hosts:[,]}'''
        data = request.data
        datas = fiddlerExe.getDatas(data['hosts'])
        datas = fiddlerExe.quchonga(datas)

        return Response(dict({'results':datas},**{"count":len(datas)}))


class dealFiddlerNotSql(GenericAPIView):
    '''myweb用例表中不存在则保存'''
    def post(self,request):
        '''body传参{hosts:[,]}'''
        data = request.data
        datas = fiddlerExe.getDatas(data['hosts'])
        datas = fiddlerExe.quchonga(datas)

        list1 = []
        case_result = casenew.objects.all()
        for case in case_result:
            url = case.url
            method = case.get_method_display()
            values = (url, method)
            # values=(valueUrl,valuem,valuedo,valueMethod)
            if values not in list1:
                list1.append(values)
        resultDatas1=[]
        for data in datas:

            if (data['url'],data['request_method']) not in list1:
                resultDatas1.append(data)



        return Response(dict({'results':resultDatas1},**{"count":len(resultDatas1)}))

class dealFiddler(GenericAPIView):
    def post(self,request):
        '''body传参{hosts:[,]}'''
        data = request.data
        datas = fiddlerExe.getDatas(data['hosts'])


        return Response(dict({'results':datas},**{"count":len(datas)}))

class fileList(GenericAPIView):
    queryset = filetest.objects.all()
    serializer_class = fileModelSerializer

    def post(self,request):
        '''新增'''

        serialize = self.get_serializer(data=request.data)
        try:
            serialize.is_valid(raise_exception=True)
        except:
            return Response(serialize.errors)
        serialize.save()
        return Response(serialize.data)

    def get(self,request):
        '''查询'''
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)


        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)


class fileInfo(GenericAPIView):
    queryset = filetest.objects.all()
    serializer_class = fileModelSerializer
    def get(self, request, pk):
        '''详情'''
        pro=self.get_object()
        return Response(self.get_serializer(pro).data)


    def put(self, request, pk):
        '''修改'''
        pro = self.get_object()
        # datas=json.loads(request.body.decode('utf-8'))
        datas=request.data
        serialize=self.get_serializer(data=datas)
        try:
            serialize.is_valid(raise_exception=True)
        except:
            return Response(serialize.errors)
        pro.file= serialize.validated_data['file']
        pro.save()
        return Response(serialize.data)

    def delete(self, request,pk):
        '''删除'''
        pro = self.get_object()
        pro.delete()
        return Response(dict(self.get_serializer(pro).data,**{"msg":'删除成功'}))


class fileView(viewsets.ModelViewSet):
    serializer_class = fileModelSerializer

    def get_queryset(self):
        return filetest.objects.all()