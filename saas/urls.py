
from django.urls import  path,re_path ,include,reverse

from . import views

urlpatterns = [
    # path('', views.index),
    path('test/', views.test),
    path('time/', views.gettime),
    path('log/', views.data_excute),
    path('project/', views.project, name="project"),
    # path('model/', views.model, name="project"),
    path('casesnew/', views.case, name="cases"),
    path('run/', views.runtest, name="run"),
    path('result/', views.result, name="result"),
    path('result_one_thread/', views.result_one_thread, name="result_one_thread"),
    path('result_last/', views.result_last, name="result_last"),
    path('download/', views.download, name="download"),


    # path('celerytest',views.login_ip, name="login_ip"),
    # path('logs/', views.logs, name="logs"),
    # path('logsx/', views.logsx, name="logsx"),
    #  path('httest/', views.httest, name="httest"),
    # path('httest/', views.IndexView.as_view(), name="httest"),

     path('projects/<int:pk>', views.projectInfo.as_view()),
     path('projects/', views.projectList.as_view()),
     path('modules/', views.moduleList.as_view()),
     path('modules/<int:pk>', views.moduleInfo.as_view()),
     path('cases/', views.caseList.as_view()),
     path('cases/<int:pk>', views.caseInfo.as_view()),
     path('relations/', views.relationList.as_view()),
     path('relations/<int:pk>', views.relationInfo.as_view()),
     path('deleteAuto/',views.deleteAuto),
     path('dealFiddlerOnly/', views.dealFiddlerOnly.as_view()),
     path('dealFiddlerNotSql/', views.dealFiddlerNotSql.as_view()),
     path('dealFiddler/', views.dealFiddler.as_view()),
     path('files/<int:pk>', views.fileInfo.as_view()),
     path('files/', views.fileList.as_view()),
     re_path(r'^file/$', views.fileView.as_view({'get':'list'})),
]