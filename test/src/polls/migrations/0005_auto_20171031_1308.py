# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-31 05:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_ptype_locked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollitem',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]