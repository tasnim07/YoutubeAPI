from youtube.models import YoutubeVideo
from serializers import VideoSerializer

from rest_framework import generics


class VideoList(generics.ListCreateAPIView):
	queryset = YoutubeVideo.objects.all()
	serializer_class = VideoSerializer

