import random
import httplib2
import json
import requests
import datetime

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets

from models import GoogleAccount, YoutubeVideo

from django.http import Http404
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect

def index(request):
    return HttpResponse('Hello world')

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
                                   scope='https://www.googleapis.com/auth/youtube',
                                   redirect_uri='http://localhost:8000/youtube/callback')
	credentials = flow.step2_exchange(code)
	access_token = credentials.access_token

	try:
		google_user = GoogleAccount.objects.get(access_token=access_token)
		user = google_user.user
	except:
		# New user
		# FIXME: Doing it temporarily to create user object with random id. Will fix it.
		username = str(random.choice(range(1, 1000)))
		user = User(username=username, password='#!', email=username + '@random.com')
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
	import pdb;pdb.set_trace()
	user = request.user
	try:
		google_user = GoogleAccount.objects.get(user=user)
	except GoogleAccount.DoesNotExist:
		raise Http404()

	channel_id = request.GET.get('channel', 'UCMDV6J2hWXet7ZCfgrXGgeg')
	url = 'https://www.googleapis.com/youtube/v3/search'
	params = {
		'part': 'snippet',
		'channelId': channel_id,
		'type': 'video',
		'videoCaption': 'any',
		'access_token': google_user.access_token,		
	}
	r = requests.get(url, params=params)
	#content = r.content
	
	content = r.json()
	items = content.get('items')
	# Store into YoutubeVideo table
	for i in range(len(items)):
		title = items[i].get('snippet').get('title')
		description = items[i].get('snippet').get('description')
		published_at = items[i].get('snippet').get('publishedAt')
		channel_id = items[i].get('snippet').get('channelId')
		video_id = items[i].get('id').get('videoId')
		video_list = YoutubeVideo(title=title, description=description, published_at=published_at, video_id=video_id, channel_id=channel_id)
		video_list.save()
	 
	# datetime.datetime.strptime('2015-09-14T07:31:08.000Z', '%Y-%m-%dT%H:%M:%S.000z')
	return redirect(reverse('video-list'))
