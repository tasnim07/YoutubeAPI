from django.shortcuts import render, HttpResponse, redirect

from oauth2client.client import flow_from_clientsecrets
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from django.core.urlresolvers import reverse
from django.http import Http404
import json
import requests

def index(request):
    return HttpResponse('Hello world')

def google_login(request):
	flow = flow_from_clientsecrets('/Users/lxidd/Desktop/client_secrets.json',
                                   scope='https://www.googleapis.com/auth/youtube',
                                   redirect_uri='http://localhost:8000/youtube/callback')
	auth_uri = flow.step1_get_authorize_url()
	return redirect(auth_uri)

def google_login_callback(request):
	code = request.GET.get('code')
	if not code:
		return HttpResponse("Oops! We couldn't authenticate!")
	flow = flow_from_clientsecrets('/Users/lxidd/Desktop/client_secrets.json',
                                   scope='https://www.googleapis.com/auth/youtube',
                                   redirect_uri='http://localhost:8000/youtube/callback')
	credentials = flow.step2_exchange(code)
	print credentials.access_token
	http = httplib2.Http()
	http_auth = credentials.authorize(http)
	youtube_data = build('youtube', 'v3', http=http_auth)
	storage = Storage('credentials')
	storage.put(credentials)
	return redirect(reverse('index'))

def list_youtube_videos(request):
	import pdb; pdb.set_trace()
	
	storage = Storage('credentials')
	credentials = storage.get()
	access_token = credentials.access_token

	url = 'https://www.googleapis.com/youtube/v3/search'
	params = {
		'part': 'snippet',
		'channelId': 'UCMDV6J2hWXet7ZCfgrXGgeg',
		'type': 'video',
		'videoCaption': 'any',
		'access_token': access_token,		
	}
	r = requests.get(url, params=params)
	return HttpResponse(r.content)
