from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Category (models. Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, default='videos')
    slug = models.SlugField(default='', null=False, max_length=100)
    number_of_videos = models.IntegerField(blank=True, default=0)
    status = models.BooleanField(default=False, help_text='0=default, 1=hidden')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
    	return reverse('category',kwargs={'slug':self.slug})

		

class VidStream(models.Model):
	title= models.CharField(max_length=300)
	category=models.ForeignKey(Category, on_delete=models.SET_NULL,verbose_name='Category',null=True)
	uploader= models.ForeignKey(User, on_delete= models.CASCADE, verbose_name='User', null=False)
	description= models.TextField(max_length=600)
	upload_date=models.DateTimeField(auto_now_add=True)
	video=models.FileField(upload_to='videos', verbose_name='Video')
	thumb=models.ImageField(upload_to='thumbs', default='',blank=True)
	views = models.PositiveBigIntegerField(blank=True, default=0)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField (blank=True, default=0)
	slug=models.SlugField(default='',null=False, max_length=100)
	status=models.BooleanField(default=False, help_text='0=default, 1=hidden')
	id = models.AutoField(primary_key=True)
	duration=models.CharField(max_length=20, default='',null=True, blank=True)
	size=models.CharField(max_length=20, default=0)
	preview=models.FileField(upload_to='preview', null=True, blank=True,default='')
	timestamp=models.DateTimeField(auto_now_add=True, null=True, blank=True)
	last_viewed = models.DateTimeField(auto_now=True)
	
	def get_related_videos(self):
		related_by_category = VidStream.objects.filter(category=self.category).exclude(id=self.id)
		related_by_uploader = VidStream.objects.filter(uploader=self.uploader).exclude(id=self.id)
		related_by_title = VidStream.objects.filter(title__icontains=self.title).exclude(id=self.id)

		related_videos=(related_by_category | related_by_title | related_by_uploader).distinct()

		return related_videos
	
	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse ('video', kwargs={'slug':self.slug})


	class Meta:
		ordering = ['-upload_date']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(VidStream, on_delete=models.CASCADE)
  


class Comment(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	video=models.ForeignKey(VidStream, on_delete=models.CASCADE)


	




