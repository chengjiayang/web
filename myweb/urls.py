"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# from django.conf.urls import url
from django.urls import  path,re_path ,include
from django.contrib import admin
from . import views
import saas.views
from  django.views.static import serve
from  django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('saas.urls')),
    path('logs/', saas.views.logs, name="logs"),
    path('logs_one_thread/', saas.views.logs_one_thread, name="logs_one_thread"),
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})


]
