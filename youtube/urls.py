from django.conf.urls import url
from youtube import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^oauth2callback/$', views.oauth2callback, name='oauth2callback'),
]
