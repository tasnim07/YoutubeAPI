from rest_framework import serializers
from youtube.models import YoutubeVideo


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeVideo
        fields = ('id', 'title', 'description', 'published_at')