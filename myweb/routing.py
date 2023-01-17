from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, re_path
from saas.consumer import ChatConsumer
import saas.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(saas.routing.websocket_urlpatterns)

)
    })