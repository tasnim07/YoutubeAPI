# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access_token', models.CharField(max_length=50)),
                ('refresh_token', models.CharField(max_length=50, null=True)),
                ('user', models.ForeignKey(related_name='google_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeVideo',
            fields=[
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('video_id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('channel_id', models.CharField(max_length=20)),
                ('published_at', models.DateTimeField(verbose_name=b'Video published time on Youtube')),
                ('created_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='googleaccount',
            unique_together=set([('user', 'access_token', 'refresh_token')]),
        ),
    ]
