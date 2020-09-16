from __future__ import unicode_literals

from django.db import models

from polls.models import PollItem
from django.core.urlresolvers import reverse
# Create your models here.
from django.contrib.auth.models import User
# from django.conf import settings
from django.utils import timezone





class Message(models.Model):
	senduser = models.ForeignKey(User, on_delete=models.CASCADE)
	pollitem = models.ForeignKey(PollItem, on_delete=models.CASCADE)
	content = models.TextField()
	# think about inserting the number of likes to this can be sequenced upwards
	userlikes = models.ManyToManyField(User, related_name='ulikes', blank=True, default=None)
	likes = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True) #updated
	timestamp = models.DateTimeField(auto_now_add=True) #added during creation
	active = models.BooleanField(default=True)

	def __str__(self):
		return str(self.content)

	def calc_likes(self):
		totallikes = self.userlikes.count()
		self.likes = totallikes
		self.save()
		return totallikes

	#dont think the below works because the reverse should be using a url name and not class name
	def get_absolute_url(self):

		return reverse("polls_detail", kwargs={"pk":self.pollitem.pk})

	# def check_like(self, user):

	# 	if Message.objects.filter(userlikes=user):
	# 		check = True
	# 	else:
	# 		check = False

	# 	print (check)

	# 	return check






	# def get_absolute_url(self):
	# 	return reverse("MessageDetail", kwargs={"pk":self.pk})

	# def get_status(self):
	# 	# parent_id = Message.objects.get(id=self.id).parent_id
	# 	# msg = Message.objects.filter(parent_id=parent_id).first()
	# 	status = self.msgtype
	# 	return status

	# def get_user_name(self):
	# 	try:
	# 		user = self.senduser.student.first_name
	# 	except:
	# 		user = self.senduser.teacher.first_name
	# 	return user


	# class Meta:
	# 	ordering = ["-timestamp","title"] #reversing the order of the entries




# class Message(models.Model):

# 	senduser = models.ForeignKey(settings.AUTH_USER_MODEL)
# 	touser = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='to_user')
# 	mainmessage = models.BooleanField(default=False)
# 	title = models.CharField(max_length=120) #- company opening and date
# 	re_opening = models.ForeignKey(Opening)

# 	msgtype = models.CharField(max_length=30, choices=order_status, default="Inactive")

# 	content = models.TextField()
# 	timestamp = models.DateTimeField(auto_now=True)
# 	date = models.DateField(auto_now=True)

# 	parent_id = models.PositiveIntegerField(null=True, blank=True)# if this is replied to than using the message id if now use this
# 	# paid = models.BooleanField(default=False)

# 	objects = MessageManager()

# 	def __unicode__(self):
# 		return self.title

# 	def get_absolute_url(self):
# 		return reverse("MessageDetail", kwargs={"pk":self.pk})

# 	def get_status(self):
# 		# parent_id = Message.objects.get(id=self.id).parent_id
# 		# msg = Message.objects.filter(parent_id=parent_id).first()
# 		status = self.msgtype
# 		return status

# 	def get_user_name(self):
# 		try:
# 			user = self.senduser.student.first_name
# 		except:
# 			user = self.senduser.teacher.first_name
# 		return user


# 		# parent_id = Message.objects.get(id=self.id).parent_id
# 		# msg = Message.objects.filter(parent_id=parent_id).first()
# 		# status = msg.msgtype
# 		# return status

# 	class Meta:
# 		ordering = ["-timestamp","title"] #reversing the order of the entries