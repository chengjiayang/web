# # 注：Django 2.2没有内置的ASGI支持，所以我们需自行在myproject/myproject下创建asgi.py：
#
# import os
# import django
# from channels.routing import get_default_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myweb.settings')
#
# django.setup()
#
# application = get_default_application()



import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import saas.routing
from django.urls import path,re_path
from saas.consumer import ChatConsumer,ChatConsumer_one_thread
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myweb.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        # URLRouter(
        #     saas.routing.websocket_urlpatterns  #  子应用路由
        # )
      URLRouter([
    re_path(r'chat/$', ChatConsumer.as_asgi()),
    re_path(r'chat_one_thread/$', ChatConsumer_one_thread.as_asgi()),

])
    ),
})