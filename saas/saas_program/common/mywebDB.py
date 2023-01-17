from saas.models import cases,Project,casenew,relationship,configs
from django.forms.models import model_to_dict
import os
import django
# if __name__ == '__main__':
# # 加载Django项目的配置信息
# # 看起来有点长, 不过此命令可以在项目的 manage.py 的第 7 行直接拿来用
#   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myweb.settings')
# # 导入Django，并启动Django项目
#
# django.setup()


def getCasebyId(tablename,id):

    case_result=tablename.objects.get(id=id)
    name=case_result.name
    url=case_result.url
    method = case_result.get_method_display()
    url_params = case_result.url_params
    body_params = case_result.body_params
    file = case_result.file
    code = case_result.code
    unchange =case_result.unchange
    change = case_result.change
    chinese = case_result.information
    case={"name":name,
          "url":url,
          "method":method,
          "url_params":url_params,
          "body_params":body_params,
          "file":file,
          "code":code,
          "unchange":unchange,
          "change":change,
          "information": chinese,

          'frontCase': '',
          'lastCase': '',
          'sql': '',
          'lastSql': '',
          'redis': '',
          'mongoDB': ''
          }
    return case


def lgetCasebyId(tablename,id):
    case_result=tablename.objects.get(id=id)
    # relates=relationship.objects.filter(status=True,basecase_id=id)
    try:
        file = case_result.file.url
    except:
        file = None
    case=model_to_dict(case_result)
    case.pop("related")
    case["method"]=case_result.get_method_display()
    case["file"]=file
    case['name'] = str(case['id'])
    case['is_online']=case_result.get_is_online_display()







    return case












