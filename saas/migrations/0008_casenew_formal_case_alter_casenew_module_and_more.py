# Generated by Django 4.1.4 on 2022-12-13 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('saas', '0007_remove_casenew_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='casenew',
            name='formal_case',
            field=models.IntegerField(choices=[(0, '否'), (1, '是')], default=1, verbose_name='正式的用例'),
        ),
        migrations.AlterField(
            model_name='casenew',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='saas.module', verbose_name='所属模块'),
        ),
        migrations.AlterField(
            model_name='casenew',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='saas.project', verbose_name='所属项目'),
        ),
    ]
