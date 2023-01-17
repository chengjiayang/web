# Generated by Django 4.1.4 on 2022-12-08 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('saas', '0004_alter_project_leader'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='nameEng',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='英文代码'),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='模块名称')),
                ('nameEng', models.CharField(blank=True, max_length=50, null=True, verbose_name='英文代码')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='saas.project', verbose_name='所属项目')),
            ],
            options={
                'verbose_name': '模块',
                'verbose_name_plural': '模块',
            },
        ),
    ]
