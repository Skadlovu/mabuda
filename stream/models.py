# in models.py
from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    file = models.FileField(upload_to='streams/')

class LiveStream(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    video = models.OneToOneField(Video, on_delete=models.CASCADE, null=True, blank=True)
