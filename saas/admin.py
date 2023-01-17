import json

from django.contrib import admin

# Register your models here.


from .import models
# from .models import Person,Group,Membership
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from saas.saas_program.common import mywebDB,creatCaseFile1102,configHttp
from  saas.saas_program import readConfig
from saas.saas_program import run_web
from django.shortcuts import render,HttpResponse,redirect
from .tasks import runallcase
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin,ImportExportActionModelAdmin
from import_export.fields import  Field
import tablib
from django.db.models import Max
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from django.contrib.admin.views import main as admin_views_main


# def get_paginator(request, data):
#     paginator = Paginator(data, 10)  # 默认每页展示10条数据
#      # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
#     page = request.GET.get('page')
#     try:
#          paginator_pages = paginator.page(page)
#     except PageNotAnInteger:
#          # 如果请求的页数不是整数, 返回第一页。
#          paginator_pages = paginator.page(1)
#     except InvalidPage:
#          # 如果请求的页数不存在, 重定向页面
#          return HttpResponse('找不到页面的内容')
#     return paginator_pages


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
admin.site.register(models.Project, ProjectAdmin)



# class relationAdmin(admin.StackedInline):
#     model = models.relation
#     fk_name = 'basecase'
#     extra = 1
#
# class caseAdmin(admin.ModelAdmin):
#     list_display = ("id","name",'url','method','url_params','body_params','file','code','unchange','change','information', 'project',"create_time","modify_time")
#     fields=["name",'url','method','url_params','body_params','file','code','unchange','change','information']
#     search_fields=["id","name",'url','method','information']
#     inlines = [relationAdmin]
#
#
# admin.site.register(models.cases, caseAdmin)
# admin.site.register(models.relation)

#admin.StackedInline,



class casenewResource(resources.ModelResource):

    def __init__(self, input_contract=None):
        super(casenewResource, self).__init__()
        field_list = models.casenew._meta.fields
        self.verbose_name_dict = {}
        for i in field_list:
            self.verbose_name_dict[i.name] = i.verbose_name

    def before_import_row(self, row, **kwargs):
        value = row.get('method')
        if type(value)==str:
            if value.lower() == 'post':
                value_new = 0
            elif value.lower() == 'get':
                value_new = 1
            elif value.lower() == 'delete':
                value_new = 2
            elif value.lower() == 'patch':
                value_new = 3
            elif value.lower() == 'put':
                value_new = 4

        else:
            value_new=value

        row['method'] = value_new

        online_value=row.get('is_online')
        if online_value=='是':
            online_value=1
        elif online_value=='否':
            online_value=0

        row['is_online']=online_value
    # def get_import_fields(self):
    #     fields = self.get_fields()
    #     for field in fields:
    #         field_name = self.get_field_name(field)
    #         # 如果有设置 verbose_name，则将 column_name 替换为 verbose_name, 否则维持原有的字段名。
    #         if field_name in self.verbose_name_dict.keys():
    #             field.column_name = self.verbose_name_dict[field_name]
    #     return fields

    def get_export_fields(self):
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            # 如果有设置 verbose_name，则将 column_name 替换为 verbose_name, 否则维持原有的字段名。
            if field_name in self.verbose_name_dict.keys():
                field.column_name = self.verbose_name_dict[field_name]
        return fields

    def export(self, queryset=None, *args, **kwargs):
        """
        Exports a resource.
        """

        self.before_export(queryset, *args, **kwargs)

        if queryset is None:
            queryset = self.get_queryset()
        headers = self.get_export_headers()
        data = tablib.Dataset(headers=headers)



        for obj in self.iter_queryset(queryset):
            # 个性化显示 choice 的值
            # obj.gender = gender_choice[obj.gender]

            obj.method = obj.get_method_display()
            obj.is_online =obj.get_is_online_display()


            data.append(self.export_resource(obj))





        self.after_export(queryset, data, *args, **kwargs)

        return data




    class Meta:
        model=models.casenew
        import_id_fields = ('id',)
        fields=('id', 'url',"method",'url_params','body_params','code','unchange','change',"is_online",'information')
        # exclude = ('id',)
        import_id_fields = ('id', 'url',"method",'url_params','body_params','code','unchange','change','is_online','information',)



class relationshipAdmin(admin.StackedInline):
    model = models.casenew.related.through
    fk_name = 'basecase'
    extra = 1
    autocomplete_fields = ['relatedcase']




# class PlaceholderMixin:
#     change_list_template = "saas/change_list.html"
#
#     def changelist_view(self, request, extra_context=None):
#         search_placeholder = getattr(self, "search_placeholder", False)
#         if search_placeholder:
#             extra_context = extra_context or {}
#             extra_context["search_placeholder"] = search_placeholder
#         return super().changelist_view(request, extra_context)
# def body_params(self):
#     return  str(self.title)[:10]

#admin.ModelAdmin
@admin.register(models.casenew)
class caseAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin):
    change_list_template = 'admin/saas/casenew/change_list.html'

    list_display = ("id",'information','url','method',"url_params_form","body_params_form",'file_form','code','unchange_form','change',"is_online","create_time","modify_time")
    fields=["is_online",'url','method','url_params','body_params','file','code','unchange','change','information']
    # list_editable=['information','url','method','code','change',"is_online"]
    search_fields=["id",'url','method','information']
    # search_placeholder='支持接口描述/id/用例名/请求路径/请求方法/进行查询'
    inlines = [relationshipAdmin,]
    # admin_views_main.MAX_SHOW_ALL_ALLOWED = 10000
    list_max_show_all=10000
    # list_max_show_all = 30
    list_per_page=10
    resource_class=casenewResource



    def excutecase_test(self,request,queryset):

        datas={}
        try:
            project_result = models.configs.objects.get(platform=0, status=True)
            datas = {"username": project_result.account, "password": project_result.password, "type": "password"}

        except:
            messages.error(request, "请在配置参数页面，仅启用一个测试环境下登陆账户")


        # print(request.POST)
        if datas!={}:
            environment = 'test'
            for id in request.POST.getlist(ACTION_CHECKBOX_NAME):

                case = mywebDB.lgetCasebyId(models.casenew, id)
                creatCaseFile1102.create(case, datas,environment)

            # configHttp.Http.host=None
            # configHttp.Http.header=None

            # run_web.runallcases()

            # run_web.runallcases()


            return redirect('/logs')


    def excutecase_online(self,request,queryset):
        datas = {}
        try:
            project_result = models.configs.objects.get(platform=1, status=True)
            datas = {"username": project_result.account, "password": project_result.password, "type": "password"}

        except:
            messages.error(request, "请在配置参数页面，仅启用一个线上环境下登陆账户")

        if datas != {}:
            environment='online'
            case_execute=[]
            for id in request.POST.getlist(ACTION_CHECKBOX_NAME):
                case = mywebDB.lgetCasebyId(models.casenew, id)
                case_execute.append(case)




            is_onlines=[]
            for case in case_execute:
                is_onlines.append(case["is_online"])
            if '否' in is_onlines:
                messages.error(request, "勾选用例中存在不支持线上执行接口")
            else:
                for case in case_execute:
                    creatCaseFile1102.create(case, datas,environment)





                # run_web.runallcases()

                return redirect('/logs')


    def copycase(self,request,queryset):

        for id in request.POST.getlist(ACTION_CHECKBOX_NAME):

            case = models.casenew.objects.get(id=id)
            relations = models.relationship.objects.filter(basecase_id=case.id)
            case.id = models.casenew.objects.all().aggregate(Max('id'))["id__max"]+1
            case.information=str('复制__')+case.information
            case.save()
            for relation in relations:
                relation.id = models.relationship.objects.all().aggregate(Max('id'))["id__max"]+1
                relation.basecase_id = case.id
                relation.save()
        return redirect('/admin/saas/casenew/')



    def excutecase_test_by_one_thread(self, request, queryset):

        datas = {}
        try:
            project_result = models.configs.objects.get(platform=0, status=True)
            datas = {"username": project_result.account, "password": project_result.password, "type": "password"}

        except:
            messages.error(request, "请在配置参数页面，仅启用一个测试环境下登陆账户")

        # print(request.POST)
        if datas != {}:
            environment = 'test'
            for id in request.POST.getlist(ACTION_CHECKBOX_NAME):
                case = mywebDB.lgetCasebyId(models.casenew, id)
                creatCaseFile1102.create(case, datas, environment)

            # configHttp.Http.host=None
            # configHttp.Http.header=None

            # run_web.runallcases()

            return redirect('/logs_one_thread')



    def dumplicate_execute(self,request,queryset):
        count = int(request.POST.get("count"))

        datas = {}
        try:
            project_result = models.configs.objects.get(platform=0, status=True)
            datas = {"username": project_result.account, "password": project_result.password, "type": "password"}

        except:
            messages.error(request, "请在配置参数页面，仅启用一个测试环境下登陆账户")


        if datas != {}:
            environment = 'test'
            for id in request.POST.getlist(ACTION_CHECKBOX_NAME):
                case = mywebDB.lgetCasebyId(models.casenew, id)
                creatCaseFile1102.create(case, datas, environment,count)

            return redirect('/logs')







    actions = ["excutecase_test", 'dumplicate_execute','copycase',"excutecase_online","excutecase_test_by_one_thread"]
    excutecase_test.short_description = '在测试环境执行接口'
    dumplicate_execute.short_description = '测试环境重复执行'
    excutecase_online.short_description = '在线上环境执行接口'
    copycase.short_description = '复制接口用例'
    excutecase_test_by_one_thread.short_description = '在测试环境单线程执行接口'




    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "information":
    #         kwargs["queryset"] = models.casenew.objects.filter(information=request.information)
    #     return super(caseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



@admin.register(models.configs)
class configsAdmin(admin.ModelAdmin):
    list_display = ('project',"account", "password",'platform',"status")
    # list_editable = ["account", "password","status"]
    list_per_page = 10
    search_fields = ["account", 'platform']

    def Batch_enable(self,request,queryset):
        for id in request.POST.getlist(ACTION_CHECKBOX_NAME):
            print(id)
            account1 = models.configs.objects.get(id=id)
            account1.status=True
            account1.save()



    def Batch_disable(self,request,queryset):
        for id in request.POST.getlist(ACTION_CHECKBOX_NAME):
            print(id)
            account2 = models.configs.objects.get(id=id)
            account2.status = False
            account2.save()



    actions = ["Batch_enable", 'Batch_disable']
    Batch_enable.short_description = '批量启用'
    Batch_disable.short_description = '批量禁用'









