from rest_framework import serializers
from youtube.models import YoutubeVideo


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeVideo
        fields = ('video_id', 'title', 'description', 'channel_id', 'published_at', 'created_on')