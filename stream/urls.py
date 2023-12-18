# in urls.py
from django.urls import path
from .views import create_live_stream, start_broadcast, end_broadcast, save_stream, live_stream_video_feed

app_name = 'stream'

urlpatterns = [
    path('create/', create_live_stream, name='create_live_stream'),
    path('<int:stream_id>/start/', start_broadcast, name='start_broadcast'),
    path('<int:stream_id>/end/', end_broadcast, name='end_broadcast'),
    path('<int:stream_id>/save/', save_stream, name='save_stream'),
    path('<int:stream_id>/video_feed/', live_stream_video_feed, name='live_stream_video_feed'),
]
