from django.conf.urls import url
from youtube import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.google_login, name='google_login'),
    url(r'^callback/$', views.google_login_callback, name='google_login_callback'),
    url(r'^videos/$', views.get_youtube_videos, name='video-list'),
]
