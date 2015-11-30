from rest_framework import serializers
from youtube.models import YoutubeVideo


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeVideo
        fields = ('title', 'description', 'published_at', 'video_id', 'channel_id', 'created_on')