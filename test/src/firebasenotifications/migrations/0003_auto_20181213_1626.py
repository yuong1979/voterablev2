# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-12-13 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firebasenotifications', '0002_auto_20181213_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicetoken',
            name='device_token',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
