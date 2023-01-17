from django.urls import path,re_path
from saas.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'chat/$', ChatConsumer.as_asgi()),
]