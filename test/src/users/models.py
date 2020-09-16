from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
import shutil
from django.core.files.storage import FileSystemStorage
from django.core.validators import RegexValidator
from django.contrib.admin.widgets import AdminDateWidget
from django.db.models.signals import pre_save, post_save
# from variables.models import Country, Level_Expertise, Region

# def image_upload_to(instance, filename):
# 	student_name = instance.user
# 	student_id = instance.id
# 	basename, file_extension = filename.split(".")
# 	new_filename = "%s-%s.%s" %(basename, student_id, file_extension)
# 	olddir = "%s/student_sub/%s/img" %(settings.MEDIA_ROOT, student_id)
# 	shutil.rmtree(olddir, ignore_errors=True)
# 	return "student_sub/%s/img/%s" %(student_id, new_filename)

# def doc_upload_to1(instance, filename):
# 	student_name = instance.user
# 	student_id = instance.id
# 	basename, file_extension = filename.split(".")
# 	new_filename = "%s-%s.%s" %(basename, student_id, file_extension)
# 	olddir = "%s/student_sub/%s/docs1" %(settings.MEDIA_ROOT, student_id)
# 	shutil.rmtree(olddir, ignore_errors=True)
# 	return "student_sub/%s/docs1/%s" %(student_id, new_filename)

def image_upload_to(instance, filename):
	user_id = instance.id
	# teacher_id = instance.id
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(basename, user_id, file_extension)
	olddir = "%s/users/%s/img" %(settings.MEDIA_ROOT, user_id)
	shutil.rmtree(olddir, ignore_errors=True)
	return "users/%s/img/%s" %(user_id, new_filename)








class PUser(models.Model):

	# function = models.CharField(max_length=20, null=True, blank=True)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	name = models.CharField(max_length=60, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	image = models.ImageField(blank=True, null=True, upload_to=image_upload_to, max_length=2048)
	rank = models.CharField(max_length=60, null=True, blank=True)
	score = models.IntegerField(default=0)
	banned = models.BooleanField(default=False) # user banned by admin
	trial = models.BooleanField(default=False) #the user created by admin
	subnewsletter = models.BooleanField(default=True) #open to subscribing newsletter
	member = models.BooleanField(default=False) #used to determine if the user is signed up




	substartdate = models.DateTimeField(null=True, blank=True)#paying member start date
	subenddate = models.DateTimeField(null=True, blank=True)#paying member end date - to be updated when payment issues or cancellation
	invoiceno = models.CharField(max_length=50, null=True, blank=True)#invoice for the transaction
	full_name = models.CharField(max_length=255, null=True, blank=True)
	email = models.EmailField(max_length=255, null=True, blank=True)
	stripe_id = models.CharField(max_length=255, null=True, blank=True)
	plan = models.CharField(max_length=255, null=True, blank=True)#type of plan the customer has subscribed

	alt_email = models.EmailField(max_length=255, null=True, blank=True)
	usermaxscore = models.IntegerField(default=0)
	freedays = models.IntegerField(default=0)


	memberp = models.BooleanField(default=False) #used to determine if the user is signed up
	substartdatep = models.DateTimeField(null=True, blank=True)#paying member start date
	subenddatep = models.DateTimeField(null=True, blank=True)#paying member end date - to be updated when payment issues or cancellation

	referralid = models.CharField(max_length=6, null=True, blank=False, default="None")




	def __str__(self):
		return str(self.user)

	def test(self):
		test = self.id
		# test = settings.TEST
		return test

	def get_absolute_url(self):
		return reverse('PUserDetail', kwargs={'pk': self.pk})

	def get_update(self):
		return reverse('PUserUpdate', kwargs={'pk': self.pk})




# def PUser_post_save_receiver(sender, instance, *args, **kwargs):
# 	instance.pexist = True

# post_save.connect(PUser_post_save_receiver, sender=PUser)

