# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import oauth2client.django_orm


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('youtube', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CredentialsModel',
            fields=[
                ('id', models.ForeignKey(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('credentials', oauth2client.django_orm.CredentialsField(null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='credentials',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='credentials',
            name='user',
        ),
        migrations.DeleteModel(
            name='Credentials',
        ),
    ]
