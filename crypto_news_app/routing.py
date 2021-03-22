from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import JobInfoConsumer

websocket_urlpatterns = URLRouter([
    re_path(r'ws/spider_info/$', JobInfoConsumer.as_asgi()),
])