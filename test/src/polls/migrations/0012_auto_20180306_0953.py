# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-06 01:53
from __future__ import unicode_literals

from django.db import migrations, models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20180306_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollitem',
            name='image',
            field=models.ImageField(blank=True, max_length=2048, null=True, upload_to=polls.models.pitem_image_upload_to),
        ),
    ]