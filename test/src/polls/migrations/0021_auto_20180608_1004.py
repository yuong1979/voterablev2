# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-08 02:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0020_auto_20180602_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollitem',
            name='description',
            field=models.TextField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='ptype',
            name='description',
            field=models.TextField(null=True, unique=True),
        ),
    ]
