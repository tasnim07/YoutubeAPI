from django.shortcuts import render
from django.http import HttpResponse

from youtube.models import YoutubeVideo
from serializers import VideoSerializer

from rest_framework.renderers import JSONRenderer

from rest_framework import generics


class VideoList(generics.ListCreateAPIView):
	import pdb; pdb.set_trace()
	queryset = YoutubeVideo.objects.all()
	serializer_class = VideoSerializer

"""
class JSONResponse(HttpResponse):
    
    #An HttpResponse that renders its content into JSON.
    
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def video_list(request):
    
    #List all videos
    
    if request.method == 'GET':
        videos = YoutubeVideo.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return JSONResponse(serializer.data)
"""

