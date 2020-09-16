# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-22 16:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('messaging', '0004_message_userlikes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='userlikes',
        ),
        migrations.AddField(
            model_name='message',
            name='userlikes',
            field=models.ManyToManyField(blank=True, default=None, related_name='ulikes', to=settings.AUTH_USER_MODEL),
        ),
    ]
