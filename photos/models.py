from django.db import models 
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse




class Photo(models.Model):
	uploader= models.ForeignKey(User, on_delete= models.CASCADE)
	title= models.CharField(max_length=300)
	description= models.TextField(max_length=600)
	upload_date=models.TimeField(auto_now_add=True)
	content=models.ImageField(upload_to='Uploaded_photos', verbose_name='photos')
	views = models.IntegerField(blank=True, default=0)
	likes = models.IntegerField(blank=True, default=0)
	dislikes = models.IntegerField (blank=True, default=0)

	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse ('photos-detail', kwargs={'pk':self.pk})