# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-24 09:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('variable', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollFav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('fav_user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PollItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(blank=True, max_length=2048, null=True, upload_to='polls/')),
                ('description', models.TextField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('ytubeurl', models.URLField(blank=True, null=True)),
                ('fburl', models.URLField(blank=True, null=True)),
                ('googurl', models.URLField(blank=True, null=True)),
                ('yelpurl', models.URLField(blank=True, null=True)),
                ('allowed', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('score', models.IntegerField(default=0)),
                ('posi', models.IntegerField(default=0)),
                ('nega', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'poll',
                'verbose_name_plural': 'polls',
            },
        ),
        # migrations.CreateModel(
        #     name='PollVote',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('posi', models.BooleanField(default=False)),
        #         ('nega', models.BooleanField(default=False)),
        #         ('date', models.DateTimeField(auto_now=True)),
        #         ('poll', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, to='polls.PollItem')),
        #         ('vote_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
        #     ],
        # ),
        migrations.CreateModel(
            name='Ptype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('subtopic', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, max_length=2048, null=True, upload_to='mpolls/')),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('vote_count', models.IntegerField(default=0)),
                ('c_user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='variable.TypeLocation')),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='variable.TypeTopic')),
                ('year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='variable.TypeYear')),
            ],
        ),
        migrations.AddField(
            model_name='pollitem',
            name='polltype',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='polls.Ptype'),
        ),
        migrations.AddField(
            model_name='pollitem',
            name='user_submit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pollfav',
            name='poll',
            field=models.ManyToManyField(blank=True, default=None, to='polls.PollItem'),
        ),
    ]
