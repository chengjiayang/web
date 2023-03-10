# Generated by Django 2.1.8 on 2021-12-09 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='casenew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=2000, null=True, verbose_name='用例名')),
                ('url', models.CharField(blank=True, max_length=2000, null=True, verbose_name='请求路径')),
                ('method', models.IntegerField(choices=[(0, 'POST'), (1, 'GET'), (2, 'DELETE'), (3, 'PATCH'), (4, 'PUT')], default=1, null=True, verbose_name='请求方法')),
                ('url_params', models.CharField(blank=True, max_length=2000, null=True, verbose_name='查询参数')),
                ('body_params', models.TextField(blank=True, null=True, verbose_name='body参数')),
                ('file', models.FileField(blank=True, null=True, upload_to='saas/saas_program/testFile', verbose_name='文件参数')),
                ('code', models.IntegerField(blank=True, null=True, verbose_name='返回码')),
                ('unchange', models.TextField(blank=True, null=True, verbose_name='返回结果（稳定型）')),
                ('change', models.CharField(blank=True, max_length=200, null=True, verbose_name='返回结果（内容变动型参数名）')),
                ('information', models.CharField(blank=True, max_length=200, null=True, verbose_name='接口描述')),
                ('result_log', models.TextField(blank=True, null=True, verbose_name='请求结果')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '接口用例',
                'verbose_name_plural': '接口用例',
            },
        ),
        migrations.CreateModel(
            name='cases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='用例名')),
                ('url', models.CharField(blank=True, max_length=20, null=True, verbose_name='请求路径')),
                ('method', models.IntegerField(choices=[(0, 'POST'), (1, 'GET'), (2, 'DELETE'), (3, 'PATCH'), (4, 'PUT')], default=1, null=True, verbose_name='请求方法')),
                ('url_params', models.CharField(blank=True, max_length=2000, null=True, verbose_name='查询参数')),
                ('body_params', models.TextField(blank=True, null=True, verbose_name='body参数')),
                ('file', models.CharField(blank=True, max_length=20, null=True, verbose_name='上传文件')),
                ('code', models.IntegerField(blank=True, null=True, verbose_name='返回码')),
                ('unchange', models.TextField(blank=True, null=True, verbose_name='返回结果（稳定型）')),
                ('change', models.CharField(blank=True, max_length=200, null=True, verbose_name='返回结果（内容变动型参数名）')),
                ('information', models.CharField(blank=True, max_length=200, null=True, verbose_name='接口描述')),
                ('result_log', models.TextField(blank=True, null=True, verbose_name='请求结果')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '接口用例',
                'verbose_name_plural': '接口用例',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='项目名称')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
            },
        ),
        migrations.CreateModel(
            name='relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, '前置接口'), (1, '后置接口')], verbose_name='前置/后置')),
                ('dealtype', models.IntegerField(choices=[(0, '接口取值'), (1, 'mysql内操作/取值'), (2, 'mongodb内操作/取值'), (3, 'redis内操作/取值')], default=0, verbose_name='操作类别')),
                ('dealcontent', models.TextField(null=True, verbose_name='操作方法')),
                ('resulparam', models.CharField(max_length=2000, null=True, verbose_name='参数名名称')),
                ('basecase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basecase', to='saas.cases', verbose_name='基础用例')),
                ('relatedcase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relatedcase', to='saas.cases', verbose_name='关联用例')),
            ],
            options={
                'verbose_name': '关联接口',
                'verbose_name_plural': '关联接口',
            },
        ),
        migrations.CreateModel(
            name='relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='启用')),
                ('type', models.IntegerField(choices=[(0, '前置接口'), (1, '后置接口')], verbose_name='前置/后置')),
                ('dealtype', models.IntegerField(choices=[(0, '接口取值'), (1, 'mysql内操作/取值'), (2, 'mongodb内操作/取值'), (3, 'redis内操作/取值'), (4, '不做参数处理')], default=0, verbose_name='操作类别')),
                ('dealcontent', models.TextField(blank=True, null=True, verbose_name='操作内容')),
                ('basecase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basec', to='saas.casenew', verbose_name='基础用例')),
                ('relatedcase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relatedc', to='saas.casenew', verbose_name='关联用例')),
            ],
            options={
                'verbose_name': '关联接口',
                'verbose_name_plural': '关联接口',
            },
        ),
        migrations.AddField(
            model_name='cases',
            name='project',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='saas.Project', verbose_name='所属项目'),
        ),
        migrations.AddField(
            model_name='casenew',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='saas.Project', verbose_name='所属项目'),
        ),
        migrations.AddField(
            model_name='casenew',
            name='related',
            field=models.ManyToManyField(through='saas.relationship', to='saas.casenew'),
        ),
    ]
