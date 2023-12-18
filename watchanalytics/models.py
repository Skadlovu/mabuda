from django.db import models
from videos.models import VidStream

class Analytics(models.Model):
	sesID= models.CharField(verbose_name='session ID', max_length=150, db_index=True)
	videoId = models.ForeignKey(VidStream, blank=True, null=True, default=None, on_delete=models.CASCADE)


	def __str__(self):
		return'{}'.format(self.sesID)




