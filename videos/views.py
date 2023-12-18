from .thumb_generator import thumb_generator 
from django.shortcuts import render, redirect
from . models import VidStream, Category, Comment, Like
from . forms import VideoUploadForm
from django.views.generic import ListView
from django.contrib.auth.models import User
from watchanalytics.models import Analytics
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import VideoSearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import JsonResponse
from .get_video_info import get_video_info
from datetime import timedelta
from django.utils import timezone
from . generate_preview import generate_preview
import random
from django.db.models import F,Q
from moviepy.editor import VideoFileClip, TextClip


@login_required
def like_video(request, video_id):
	video= VidStream.objects.get(pk=video_id)
	user=request.user


	if Like.objects.filter(user=user, video=video).exists():
		Like.objects.filter(user=user, video=video).delete()
		is_liked=False
	else:
		Like.objects.create(user=user, video=video)
		is_liked=True
	likes_count=Like.objects.filter(video=video).count()
	return JsonResponse({'likes_count':likes_count,'is_liked':is_liked})
	


@login_required
def create_video(request):
	template= 'videos/video_create.html'
	if request.method == 'POST':

		video_form = VideoUploadForm(request.POST, request.FILES)
		if video_form.is_valid():
			video_instance = video_form.save(commit=False)
			video_instance.uploader = request.user
			video_instance.save()

			uploaded_video=request.FILES.get('video')


			thumb_generator(video_instance.video, video_instance)
			
			formatted_duration,formatted_size=get_video_info(uploaded_video.read())

			if formatted_duration is not None and formatted_size is not None:
				video_instance.duration=formatted_duration
				video_instance.size=formatted_size
				video_instance.save()

				watermark_text = "uploaded to xxxworld"
				video_path = video_instance.video.path
				clip = VideoFileClip(video_path)
				txt_clip = TextClip(watermark_text, fontsize=24, color='white', bg_color='black')
				watermarked_clip = clip.overlay(txt_clip.set_pos(('center', 'bottom')).set_duration(clip.duration))
				watermarked_clip.write_videofile(video_path, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)


				messages.success(request,'Video uploaded successfully!!!. redirecting to the home page shortly')

				return redirect('videos:video-list')
	
			else:
				messages.error(request,'Error getting video information.')
				
				return redirect('videos:video-list')
	
		else:
			messages.error(request, 'Error uploading video. Please check the form.')
	
	else:
		video_form = VideoUploadForm()

	return render(request,template,{'video_form': video_form} )


@login_required
def post_comment(request):
	video_id=request.POST.get('video_id')
	comment_content=request.POST.get('comment')
	comment=Comment.objects.create(user=request.user, video_id=video_id,content=comment_content)
	return JsonResponse({'comment': comment.content, 'user': comment.user.username})


def videolist(request):
	videos=VidStream.objects.all()


	videos_per_page = 20

	paginator = Paginator(videos, videos_per_page)


	page = request.GET.get('page')


	try:
		videos = paginator.page(page)

	except PageNotAnInteger:

		videos = paginator.page(1)

	except EmptyPage:

		videos = paginator.page(paginator.num_pages)

	return render(request, 'videos/video-list.html', {'videos':videos})



def search(request):
    videos = []
    query = ''

    if 'title' in request.GET:
        form = VideoSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['title']
            videos = VidStream.objects.filter(title__icontains=query)
    else:
        form = VideoSearchForm()

    return render(request, 'videos/search.html', {'form': form, 'query': query, 'videos': videos})



def get_video(request, video_id):
	template='videos/video.html'
	video = VidStream.objects.get(id=video_id)
	related_videos=random.sample(list(video.get_related_videos()),5)
	categories=random.sample(list(Category.objects.all()),10)
	

	if not request.session.session_key:
		request.session.save()

	session_key= request.session.session_key
	is_views=Analytics.objects.filter(videoId=video_id, sesID=session_key)
	if is_views.count()== 0 and str(session_key) !="None":
		views=Analytics()
		views.sesID=session_key
		views.videoId=video			
		views.save()

		video.views += 1
		video.save()
	context={'video':video, 'related_videos':related_videos,'categories':categories,}
	return render(request,template,context)


def categoryView(request):
	template='videos/category.html'
	category= Category.objects.filter(status=0).order_by('name')
	context={'category':category}
	category_with_count = category.annotate(video_count=Count('vidstream'))
	context = {'category': category_with_count}
	
	category_per_page = 40
	paginator = Paginator(category, category_per_page)
	page = request.GET.get('page')

	try:
		category = paginator.page(page)
	except PageNotAnInteger:
		category = paginator.page(1)
	except EmptyPage:
		category = paginator.page(paginator.num_pages)
	
	return render(request, template, context)


def categorylist(request, slug):
	template='videos/category-list.html'
	if (Category.objects.filter(slug=slug, status=0)):
		videos=VidStream.objects.filter(category__slug=slug)
		category=Category.objects.filter(slug=slug).first()
		context={"videos":videos, 'category':category}
		videos_per_page = 20
		paginator = Paginator(videos, videos_per_page)
		page = request.GET.get('page')
		try:
			videos = paginator.page(page)
		except PageNotAnInteger:
			videos = paginator.page(1)
		except EmptyPage:
			videos = paginator.page(paginator.num_pages)
		
		
		return render(request, template, context)
	else:
		messages.warning(request, 'Category does not exist. You will be redirected to the category page momemntarily ')
		return redirect('videos/category.html')


def most_viewed_videos(request):
    # Retrieve all videos ordered by views in descending order
    most_viewed_videos = VidStream.objects.order_by('-views')

    context = {'most_viewed_videos': most_viewed_videos}
    return render(request, 'videos/most_viewed_videos.html', context)


def trending_videos(request):
    # Retrieve all videos ordered by views in descending order
    trending_videos = VidStream.objects.order_by('-views')

    # Calculate the timestamp for 24 hours ago
    twenty_four_hours_ago = timezone.now() - timezone.timedelta(hours=24)

    # Filter videos uploaded or viewed in the past 24 hours
    trending_videos = trending_videos.filter(
        Q(upload_date__gte=twenty_four_hours_ago) | Q(last_viewed__gte=twenty_four_hours_ago)
    )

    context = {'trending_videos': trending_videos}
    return render(request, 'videos/trending_videos.html', context)
