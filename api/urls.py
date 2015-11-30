from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^videos/$', views.VideoList.as_view(), name='video-list'),
]
