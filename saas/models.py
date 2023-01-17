from django.db import models

# Create your models here.




class Project(models.Model):
    name = models.CharField('项目名称', max_length=50, unique=True, null=False)
    nameEng = models.CharField('英文代码', max_length=50, null=True, blank=True)
    leader=models.CharField('负责人', max_length=50, null=True,blank=True)
    create_time=models.DateTimeField('创建时间',auto_now_add=True,null=True)
    modify_time = models.DateTimeField('更新时间', auto_now=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'


class Module(models.Model):
    name = models.CharField('模块名称', max_length=50, unique=True, null=False)
    nameEng = models.CharField('英文代码', max_length=50, null=True, blank=True)
    project = models.ForeignKey(to='Project', to_field='id', on_delete=models.SET_NULL, null=True, verbose_name='所属项目',
                                )
    create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    modify_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '模块'
        verbose_name_plural = '模块'

class cases(models.Model):
    method_values=(
                  (0,u'POST'),
                  (1,u'GET'),
                  (2,u'DELETE'),
                  (3,u'PATCH'),
                  (4,u'PUT')
                  )
    project=models.ForeignKey(to='Project',to_field='id',on_delete=models.CASCADE,null=True,verbose_name='所属项目',default=1)
    name = models.CharField('用例名',max_length=20,null=True,blank=True)
    url = models.CharField('请求路径',max_length=20,null=True,blank=True)
    # method = models.CharField('请求方法',max_length=20,null=True,blank=True)
    method = models.IntegerField(choices=method_values, null=True,verbose_name='请求方法',default=1)
    url_params = models.CharField('查询参数',max_length=2000,null=True,blank=True)
    body_params = models.TextField('body参数',null=True,blank=True)
    file = models.CharField('上传文件',max_length=20,null=True,blank=True)
    # frontCase = models.CharField(max_length=20,null=True,blank=True)
    code = models.IntegerField('返回码',null=True,blank=True)
    unchange = models.TextField(null=True,blank=True,verbose_name='返回结果（稳定型）')
    change = models.CharField(max_length=200,null=True,blank=True,verbose_name='返回结果（内容变动型参数名）')
    information = models.CharField('接口描述',max_length=200,null=True,blank=True)
    # lastCase = models.CharField(max_length=20,null=True,blank=True)
    # sql = models.CharField(max_length=20,null=True,blank=True)
    result_log =models.TextField('请求结果',null=True,blank=True)

    create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    modify_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.information

    class Meta:
        verbose_name = '接口用例'
        verbose_name_plural = '接口用例'



class relation(models.Model):
    relation_types=((0,'前置接口'),(1,"后置接口"))
    basecase=models.ForeignKey(to="cases",to_field='id',on_delete=models.CASCADE,related_name='basecase',verbose_name='基础用例')
    relatedcase = models.ForeignKey(to="cases",to_field='id',on_delete=models.CASCADE,related_name='relatedcase',verbose_name='关联用例')
    type=models.IntegerField(choices=relation_types,verbose_name='前置/后置')
    dealtypes = ((0, "接口取值"), (1, "mysql内操作/取值"), (2, "mongodb内操作/取值"), (3, "redis内操作/取值"))
    dealtype = models.IntegerField(choices=dealtypes, verbose_name='操作类别',default=0)
    dealcontent = models.TextField(null=True, verbose_name='操作方法')
    resulparam = models.CharField(max_length=2000, null=True, verbose_name='参数名名称')

    def __str__(self):
        return self.relatedcase

    class Meta:
        verbose_name = '关联接口'
        verbose_name_plural ='关联接口'



class casenew(models.Model):
    id = models.AutoField(primary_key=True)
    method_values=(
                  (0,u'POST'),
                  (1,u'GET'),
                  (2,u'DELETE'),
                  (3,u'PATCH'),
                  (4,u'PUT')
                  )

    project=models.ForeignKey(to='Project',to_field='id',on_delete=models.SET_NULL,null=True,verbose_name='所属项目',blank=True)
    module=models.ForeignKey(to='Module',to_field='id',on_delete=models.SET_NULL,null=True,verbose_name='所属模块',blank=True)
    # name = models.CharField(verbose_name='用例名',max_length=2000,null=True,blank=True)
    url = models.CharField(verbose_name='请求路径',max_length=2000,null=True,blank=True)
    # method = models.CharField('请求方法',max_length=20,null=True,blank=True)
    method = models.IntegerField(choices=method_values, null=True,verbose_name='请求方法',default=1)
    url_params = models.CharField(verbose_name='查询参数',max_length=2000,null=True,blank=True)
    body_params = models.TextField(verbose_name='body参数',null=True,blank=True )
    file = models.CharField(max_length=2000,verbose_name='文件参数',null=True,blank=True)
    # frontCase = models.CharField(max_length=20,null=True,blank=True)
    code = models.IntegerField(verbose_name='返回码',null=True,blank=True)
    unchange = models.TextField(null=True,blank=True,verbose_name='返回结果（稳定型）')
    change = models.CharField(max_length=200,null=True,blank=True,verbose_name='返回结果（内容变动型参数名）')
    information = models.CharField(verbose_name='接口描述',max_length=200,null=True,blank=True)
    # lastCase = models.CharField(max_length=20,null=True,blank=True)
    # sql = models.CharField(max_length=20,null=True,blank=True)
    result_log =models.TextField(verbose_name='请求结果',null=True,blank=True)

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True)
    modify_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, null=True)

    related=models.ManyToManyField(to="self",
                                   through='relationship',through_fields=('basecase','relatedcase'),symmetrical=False, null=True
                                   )
    choice = ((0, '否'), (1, '是'))
    is_online=models.BooleanField(verbose_name='可线上执行',default=False)
    formal_case=models.BooleanField(verbose_name='正式的用例',default=True)



    def __str__(self):
        return self.information

    class Meta:
        verbose_name = '接口用例'
        verbose_name_plural = '接口用例'

    def body_params_form(self):
        if len(str(self.body_params))>30:
            return '{body_params}……'.format(body_params=str(self.body_params)[:30])
        else:
            return str(self.body_params)

    body_params_form.allow_tags = True
    body_params_form.short_description='body参数'


    def url_params_form(self):
        if len(str(self.url_params))>30:
            return '{body_params}……'.format(body_params=str(self.url_params)[:30])
        elif self.url_params==None:
            return ''
        else:
            return str(self.url_params)

    url_params_form.allow_tags = True
    url_params_form.short_description = '查询参数'


    def unchange_form(self):
        if len(str(self.unchange))>30:
            return '{body_params}……'.format(body_params=str(self.unchange)[:30])
        else:
            return str(self.unchange)

    unchange_form.allow_tags = True
    unchange_form.short_description = '返回结果（稳定型）'


    def file_form(self):
        if len(str(self.file))>30:
            return '{body_params}……'.format(body_params=str(self.file)[-30:])
        else:
            return str(self.file)

    file_form.allow_tags = True
    file_form.short_description = '文件参数'

    # def get_is_online_display(self):
    #     if self.is_online:
    #         return '支持'
    #     else:
    #         return '不支持'

    # get_is_online.allow_tags = True
    # get_is_online.short_description = '可线上执行'










    # def url_params_form(self):
    #     return str(self.title)[:10]


class relationship(models.Model):
    status = models.BooleanField(verbose_name='启用', default=False)
    # step=models.IntegerField(verbose_name='第x步', default=1)
    basecase = models.ForeignKey(to="casenew", to_field='id', on_delete=models.CASCADE, related_name='basec',
                                 verbose_name='基础用例')
    relatedcase = models.ForeignKey(to="casenew", to_field='id', on_delete=models.CASCADE, related_name='relatedc',
                                    verbose_name='关联用例', null=True)
    relation_types = ((0, '前置接口'), (1, "后置接口"))
    type = models.IntegerField(choices=relation_types, verbose_name='前置/后置')

    # dealtypes = ((0, "获取接口返回值"), (1, "mysql操作"), (2, "mongodb操作"), (3, "redis操作"),(4,'无后续操作'),(5,'仅获取接口query请求值'),(6,'仅获取接口body请求值'))
    # dealtype = models.IntegerField(choices=dealtypes, verbose_name='数据操作类别',default=4)

    # getResult= models.BooleanField(verbose_name='调用接口后取返回值', default=True)
    interfaceProcess = models.CharField('从接口返回中取值字典', max_length=2000, null=True, blank=True)

    # dealId=models.ForeignKey(to='deals',to_field="id",on_delete=models.CASCADE,related_name='deal',verbose_name='数据处理方案',null=True)
    # resulparam = models.CharField(max_length=2000, null=True, verbose_name='参数名名称',blank=True)


    # dealtypes = ((0, '接口取值'), (1, "mysql"), (2, "mongodb"), (3, "redis"))
    # type = models.IntegerField(choices=dealtypes, verbose_name='mongodb操作类别', default=0)

    sqls = models.TextField(null=True, verbose_name='mysql数据库语句', blank=True)
    mdealtypes = ((0, "select"), (1, "update"),(2,"无操作"))
    m_type = models.IntegerField(choices=mdealtypes, verbose_name='mongodb操作类别',default=3)
    m_table = models.CharField('mongodb操作表', max_length=2000, null=True, blank=True)
    m_query = models.CharField('mongodb查询条件', max_length=2000, null=True, blank=True)
    m_order = models.CharField('mongodb排序条件', max_length=2000, null=True, blank=True)
    m_result = models.CharField('mongodb目的参数', max_length=2000, null=True, blank=True)
    interfaceRequest_url = models.CharField('从接口请求查询参数中取值字典', max_length=2000, null=True, blank=True)
    interfaceRequest_body = models.CharField('从接口请求body参数中取值字典', max_length=2000, null=True, blank=True)

    # dealcontent = models.TextField(null=True, verbose_name='操作内容', blank=True)
    def __str__(self):
        return str(self.relatedcase)

    class Meta:
        verbose_name = '数据构造/处理'
        verbose_name_plural ='数据构造/处理'









class configs(models.Model):
    account=models.CharField('测试账号',max_length=2000,null=False)
    password = models.CharField('测试账号密码', max_length=2000, null=False)
    platforms=mdealtypes = ((0, "测试环境"), (1, "线上环境"))
    platform = models.IntegerField(choices=platforms, verbose_name='测试平台', default=0)
    project=models.ForeignKey(to='Project',to_field='id',on_delete=models.CASCADE,null=True,verbose_name='所属项目')
    status = models.BooleanField(verbose_name='启用', default=False)


    class Meta:
        verbose_name = '参数配置'
        verbose_name_plural ='参数配置'



class filetest(models.Model):
    file = models.FileField(verbose_name='文件参数', null=True, blank=True, upload_to='saas/saas_program/testFile')

    class Meta:
        verbose_name = '文件管理'
        verbose_name_plural ='文件管理'















# class Person(models.Model):
#     name = models.CharField(max_length=50)
#
# class Group(models.Model):
#     name = models.CharField(max_length=128)
#     members = models.ManyToManyField(
#     Person,
#     through='Membership',
#     through_fields=('group', 'person'),
#     )
#
# class Membership(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     person = models.ForeignKey(Person, on_delete=models.CASCADE)
#     inviter = models.ForeignKey(
#     Person,
#     on_delete=models.CASCADE,
#     related_name="membership_invites",
#     )
#     invite_reason = models.CharField(max_length=64)



















