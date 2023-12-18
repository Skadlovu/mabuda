from . import views
from. views import PhotoDetailView, UserPhotoListView, PhotoCreateView, GeneralPhotoListView, PhotoDeleteView
from django.urls import path




urlpatterns= [
	path('photo-list/', GeneralPhotoListView.as_view(template_name='photos/photo-list.html'),name='photo-list'),
	path('photos/photo-detail/<int:pk>',PhotoDetailView.as_view(template_name='photos/photo-detail.html'),name='photo-detail'),
	path('<int:pk>delete/', PhotoDeleteView.as_view(template_name='photos/photo-confirm-delete.html'),name='photo-delete'),
	path('user/<str:username>',UserPhotoListView.as_view(template_name='photos/user-photos-list.html'),name='user-photo'),
	path('photo/new/', PhotoCreateView.as_view(template_name='photos/photo_create'),name='photo_create'),


]