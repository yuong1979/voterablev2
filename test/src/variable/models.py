from __future__ import unicode_literals

from django.db import models

# Create your models here.




class TypeTopic(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class TypeYear(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class TypeLocation(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title