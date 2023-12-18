from django import forms 
from . models import VidStream

class VideoUploadForm(forms.ModelForm):

	class Meta:
		model= VidStream
		fields= ['category','title', 'description', 'video']


class VideoSearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, label='Search by Title')
	

