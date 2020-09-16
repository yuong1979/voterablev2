# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-18 08:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('firebasenotifications', '0004_devicetoken_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicetoken',
            name='userdt',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
