# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-20 01:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_auto_20171119_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scorepollitemsbymonth',
            name='month',
            field=models.CharField(max_length=3),
        ),
    ]
