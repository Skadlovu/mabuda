from django.shortcuts import render, redirect, get_object_or_404
from . models import Photo
from . forms import PhotoUploadForm
from django.views.generic import DetailView, DeleteView, UpdateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User



class PhotoCreateView(LoginRequiredMixin, CreateView):
	model= Photo
	success_url=('/')
	template_name='photos/post_create.html'
	fields= [ 'title', 'description', 'content']


	def form_valid(self,form):
		form.instance.profiles= self.request.user
		return super().form_valid(form)


	def test_func(self):
		content= self.get_object()
		if self.request.user== content.uploader:
			return True
		return False





class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	template_name= 'photos/photo-confirm-delete.html'
	success_url='/'
	model=Photo

	def test_func(self):
		content=self.get_object()
		if self.request == content.uploader:
			return True
		return False


 

class UserPhotoListView(ListView):
	model= Photo
	template_name= 'photos/user-photos.html'
	context_object_name='content'

	def get_quaryset(self):
		user= get_object_or_404(User, username=self.kwargs.get('username'))
		return Vidstream.objects.filter(uploader=username).order_by('-upload_date')




class PhotoDetailView(DetailView):
	template_name= 'photos/photos-detail.html'
	model= Photo



class GeneralPhotoListView(ListView):
	model= Photo
	template_name= 'photos/photos-list.html'
	context_object_name= 'content'
	ordering= ['-upload_date']




def search(request):
	if request.method== 'POST':
		query=request.POST.get('title', None)
		if query:
			results= Photo.objects.filter(title_contains= query)
			return render(request, 'photos/search.html'), {'content':results}
	return render(request('photos/search.html'))

