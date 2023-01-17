from saas.saas_program.common import  comReport
import os
import datetime
from django.forms.models import model_to_dict
if __name__ == '__main__':
# 加载Django项目的配置信息
# 看起来有点长, 不过此命令可以在项目的 manage.py 的第 7 行直接拿来用
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myweb.settings')
# 导入Django，并启动Django项目
import django
django.setup()

# 然后就可以直接通过此py文件进行调试了
from saas.models import *
# ret = models.Person.object.all()
# print(ret)

# relations_front=relationship.objects.filter(status=True,basecase_id=4,type=0)
# case=relations_front[0].relatedcase
# case.method=case.get_method_display()
# case = model_to_dict(case)
# print(case)

# print(relations_front[0].dealcontent)

# start_time = datetime.datetime.now()
# comReports = comReport.Report()
# end_time = datetime.datetime.now()
# comReport.Report.datas = comReports.datas_processing()
# comReports.merge_reports(start_time, end_time - start_time)
# comReports.create_report_email(start_time, end_time - start_time)

# case = casenew.objects.get(id=4)
# case=model_to_dict(case)

case_result = casenew.objects.get(id=8)
# relates=relationship.objects.filter(status=True,basecase_id=6)
print(case_result.file.url)
#
# case = model_to_dict(case_result)
#
#
# case.pop("related")
# case["method"] = case_result.get_method_display()
# case["file"]=file

#
# f = open(r'.', "rb")
# print(f.read())
# print(relates.values())

# fileParam

print('/saas/saas_program/testFile/srchttp___img.jj20.com_up_allimg_tp05_1910021S351A06-0-lp.jpg_4xFsvOr.jpg'.split("/saas/saas_program/testFile/")[1])