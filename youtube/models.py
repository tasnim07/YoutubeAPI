import pickle
import base64

from django.db import models
from django.contrib.auth.models import User

from oauth2client.django_orm import FlowField
from oauth2client.django_orm import CredentialsField

class GoogleAccount(models.Model):
	"""A model to hold the Google login records.
	"""
	access_token = models.CharField(max_length=50)
	user = models.ForeignKey(User, related_name='google_user')
	refresh_token = models.CharField(max_length=50, null=True)

	class Meta:
		unique_together = ('user', 'access_token', 'refresh_token')

	def __str__(self):
		return self.user.email


class YoutubeVideo(models.Model):
	"""A model to hold the Youtube videos information
	"""
	title = models.CharField(max_length=100)
	description = models.TextField(null=True)
	video_id = models.CharField(max_length=20, primary_key=True)
	# INFO: Not sure if we need to store this but could be 
	# useful to get videos by channel id from the DB instantly.
	channel_id = models.CharField(max_length=20)
	published_at = models.DateTimeField(verbose_name='Video published time on Youtube')
	created_on = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title
