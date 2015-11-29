from django.shortcuts import render, HttpResponse

from oauth2client.client import flow_from_clientsecrets

def index(request):
    return HttpResponse('Hello world')

def oauth2callback(request):
    flow = flow_from_clientsecrets('/Users/lxidd/Desktop/client_secrets.json',
                                   scope='https://www.googleapis.com/auth/youtube',
                                   redirect_uri = 'http://locathost:8000/oauth2callback')
    return HttpResponse(flow)

