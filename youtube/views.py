#System imports
import json
import datetime

#Third party library imports
import requests
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets

#Application import
from models import GoogleAccount, YoutubeVideo

#Django imports
from django.http import Http404
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect

def google_login(request):
	flow = flow_from_clientsecrets('/Users/lxidd/Desktop/client_secrets.json',
                                   scope='https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/userinfo.email',
                                   redirect_uri='http://localhost:8000/youtube/callback')
	auth_uri = flow.step1_get_authorize_url()
	return redirect(auth_uri)

def google_login_callback(request):
	code = request.GET.get('code')
	if not code:
		return HttpResponse("Oops! We couldn't authenticate!")

	# FIXME: I have hard-coded the client secrets file path for now.
	flow = flow_from_clientsecrets('/Users/lxidd/Desktop/client_secrets.json',
                                   scope='https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/userinfo.email',
                                   redirect_uri='http://localhost:8000/youtube/callback')
	credentials = flow.step2_exchange(code)
	access_token = credentials.access_token

	#Get the user email address.
	params = {
		'access_token': access_token
	}
	r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=params)
	content = r.json()
	email = content.get('email')

	try:
		google_user = GoogleAccount.objects.get(access_token=access_token)
		user = google_user.user
	except:
		# New user
		user = User(username=email.split('@')[0], password='#!', email=email)
		user.save()
		google_user = GoogleAccount(user=user, access_token=access_token)
		google_user.save()

	user.backend = 'django.contrib.auth.backends.ModelBackend'
	login(request, user)

	return redirect(reverse('video-list'))

@login_required
def get_youtube_videos(request):
	"""Returns list of all the youtube videos by
	channel id.
	"""
	user = request.user
	try:
		google_user = GoogleAccount.objects.get(user=user)
	except GoogleAccount.DoesNotExist:
		raise Http404()

	channel_id = request.GET.get('channel','UC6-F5tO8uklgE9Zy8IvbdFw') #'UCMDV6J2hWXet7ZCfgrXGgeg'
	url = 'https://www.googleapis.com/youtube/v3/search'
	params = {
		'part': 'snippet',
		'channelId': channel_id,
		'type': 'video',
		'videoCaption': 'any',
		'access_token': google_user.access_token,		
	}
	r = requests.get(url, params=params)
	content = r.json()
	
	# Store into YoutubeVideo table
	items = content.get('items')
	for i in range(len(items)):
		title = items[i].get('snippet').get('title')
		description = items[i].get('snippet').get('description')
		published_at = items[i].get('snippet').get('publishedAt')
		channel_id = items[i].get('snippet').get('channelId')
		video_id = items[i].get('id').get('videoId')
		video_info = YoutubeVideo(title=title, description=description, published_at=published_at, video_id=video_id, channel_id=channel_id)
		video_info.save()
	 
	# datetime.datetime.strptime('2015-09-14T07:31:08.000Z', '%Y-%m-%dT%H:%M:%S.000z')
	return redirect(reverse('video-list'))
