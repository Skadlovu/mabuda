from . import views
from django.urls import path


app_name='videos'

urlpatterns= [
	path('videos/new/', views.create_video, name='video_create'),
	path('videos/search/',views.search, name='search'),
	path('videos/video/<video_id>', views.get_video, name='video'),
	path('videos/category/', views.categoryView, name='category'),
	path('videos/category-list <str:slug>/', views.categorylist,name='category-list'),
	path('', views.videolist, name='video-list'),
    path('api/comments/', views.post_comment, name='post_comment'),
    path('videos/trending_videos', views.trending_videos, name='trending_videos'),
    path('videos/most_viewed_videos', views.most_viewed_videos, name='most_viewed_videos'),
    path('like-video/<int:video_id>', views.like_video, name='like_video')


]



	#path('videos/category/', CategoryListView.as_view(template_name='videos/category.html'),name='category'),
# path('videos/video/<int:pk>/',VideoDetailView.as_view(),name='video'),
# path('videos/new/', VideoCreateView.as_view(template_name='videos/video_create.html'),name='video_create'),
	#path('videos/<int:pk>delete/', VideoDeleteView.as_view(),name='video-delete'),
# path('', GeneralVideoListView.as_view(),name='video-list'),
