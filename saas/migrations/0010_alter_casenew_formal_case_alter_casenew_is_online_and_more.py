# Generated by Django 4.1.4 on 2022-12-16 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saas', '0009_remove_relationship_dealtype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casenew',
            name='formal_case',
            field=models.BooleanField(default=True, verbose_name='正式的用例'),
        ),
        migrations.AlterField(
            model_name='casenew',
            name='is_online',
            field=models.BooleanField(default=False, verbose_name='可线上执行'),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='m_type',
            field=models.IntegerField(blank=True, choices=[(0, 'select'), (1, 'update')], null=True, verbose_name='mongodb操作类别'),
        ),
    ]