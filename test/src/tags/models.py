from __future__ import unicode_literals

from django.db import models

# Create your models here.
from polls.models import Ptype
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.conf import settings

def runtagcount():

	#if you want to deactivate a tag, you need to remove all the polls it is attached to first
	tagcounter = TagPoll.objects.all()

	for i in tagcounter:
		i.counter = i.polltype.filter(active=True).count()

		# if the number of polls in the tag is zero then label for the tag is deactivated
		if i.counter == 0:
		    i.active = False
		else:
		    i.active = True

		i.save()



class TagPoll(models.Model):
	title = models.CharField(max_length=120, unique=True)
	polltype = models.ManyToManyField(Ptype)
	active = models.BooleanField(default=True)
	counter = models.IntegerField(default=0)
	tagfav = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, default=None)

	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		return reverse("TagView", kwargs={"pk":self.pk})



class TopicPoll(models.Model):
	title = models.CharField(max_length=100, unique=True)
	Tagtype = models.ManyToManyField(TagPoll)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=False)
	counter = models.IntegerField(default=0)
	tagfav = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, default=None)


	def __str__(self):
		return self.title

	# def get_absolute_url(self):
	# 	return reverse("TopicView", kwargs={"pk":self.pk})

	# #Override models save method to clean tag field:
	# def save(self, *args, **kwargs):
	# 	super(TagPoll, self).save(*args, **kwargs)
	# 	#Only set the slug when the object is created.

	# 	if self.id:
	# 		# print (self.id)
	# 		# print (self.title)
	# 		# print (self.polltype.count())

	# 		activeptypes = self.polltype.filter(active=True).count()

	# 		self.counter = activeptypes
	# 		print (self.title)
	# 		print (self.counter)

	# 		if activeptypes == 0:
	# 			self.active = False
	# 		else:
	# 			self.active = True

	# 		super(TagPoll, self).save(*args, **kwargs)

	# 		# for i in self.polltype.filter(active=True):
	# 		# 	print (i)






# , on_delete=models.CASCADE