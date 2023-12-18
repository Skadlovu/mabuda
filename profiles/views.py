from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . forms import UserRegistrationForm, UserUpdateForm, UserProfileUpdateForm
from django.contrib.auth.models import User
from videos.models import VidStream
from .models import Profile


def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else: 
		form=UserRegistrationForm()
	return render(request, 'profiles/register.html', {'form': form})


@login_required
def profile(request):
	if request.method == 'POST':
		userform=UserUpdateForm(request.POST, instance=request.user)
		profileform= UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if userform.is_valid() and profileform.is_valid():
			userform.save()
			profileform.save()
			return redirect('profile')
	else: 
		userform=UserUpdateForm(instance=request.user)
		profileform=UserProfileUpdateForm(instance=request.user.profile)
		#change_password_form=ChangePasswordForm(instance=request.user)
	
	videos=VidStream
	while videos.uploader == Profile.user:
			videos.video.all(videos.uploader)
		

	context ={
		'userform':userform,
		'profileform': profileform,
	}
	return render(request, 'profiles/profile.html', context)


