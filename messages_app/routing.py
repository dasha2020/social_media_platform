from django.urls import re_path
from . import consumers
from channels.db import database_sync_to_async

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi(), name="chat_room"),
]