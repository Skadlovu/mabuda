from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/live_stream/(?P<live_stream_id>\d+)/chat/$', consumers.ChatConsumer.as_asgi()),
]
