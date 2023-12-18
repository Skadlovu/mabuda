# in views.py
import cv2
from django.views.decorators import gzip
from django.contrib.auth.decorators import login_required
from .models import LiveStream, Video
import threading
import time
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.http import StreamingHttpResponse
from django_q.tasks import async_task

def generate_frames(live_stream):
    while True:
        if not live_stream.is_active:
            break
        success, frame = cv2.VideoCapture(0).read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0.1)

@login_required
def create_live_stream(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        start_time = timezone.now()
        creator = request.user

        video = Video.objects.create(file=None)
        live_stream = LiveStream.objects.create(
            title=title,
            description=description,
            start_time=start_time,
            creator=creator,
            is_active=True,
            video=video
        )

        # Start the background task for live streaming
        async_task('your_app.views.live_stream_live_video', live_stream.id)

        # Redirect to the live broadcast page
        return redirect('stream:start_broadcast', stream_id=live_stream.id)

    return render(request, 'stream/create_live_stream.html')

@login_required
def live_stream_live_video(stream_id):
    live_stream = get_object_or_404(LiveStream, pk=stream_id)
    
    # OpenCV streaming code
    cap = cv2.VideoCapture(0)
    while live_stream.is_active:
        success, frame = cap.read()
        if not success:
            break
        live_stream.video.file.save('stream.mp4', ContentFile(frame.tobytes()))

    cap.release()

@login_required
def start_broadcast(request, stream_id):
    live_stream = get_object_or_404(LiveStream, pk=stream_id, creator=request.user)
    return render(request, 'stream/start_broadcast.html', {'live_stream': live_stream})

@login_required
def end_broadcast(request, stream_id):
    live_stream = get_object_or_404(LiveStream, pk=stream_id, creator=request.user)
    live_stream.is_active = False
    live_stream.save()
    return redirect('stream:save_stream', stream_id=live_stream.id)

@login_required
def save_stream(request, stream_id):
    live_stream = get_object_or_404(LiveStream, pk=stream_id)
    return render(request, 'stream/save_stream.html', {'live_stream': live_stream})

@gzip.gzip_page
def live_stream_video_feed(request, stream_id):
    live_stream = get_object_or_404(LiveStream, pk=stream_id)

    def generate():
        while live_stream.is_active:
            success, frame = cv2.VideoCapture(0).read()
            if not success:
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            time.sleep(0.1)

    return StreamingHttpResponse(generate(), content_type="multipart/x-mixed-replace;boundary=frame")
