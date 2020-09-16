from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from polls.models import PollItem, Ptype
from django.utils import timezone
from django.conf import settings
import pytz
import string
import random

# Create your models here.

class ViewPollTypeUnique(models.Model):
	p_type = models.OneToOneField(Ptype, blank=True, default=None, on_delete=models.CASCADE)
	userview = models.ManyToManyField(User, blank=True, default=None)
	vcount = models.IntegerField(default=0)#counting the number views
	ecount = models.IntegerField(default=0)#counting the number of entries on a poll type
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.p_type)

	def get_user_count(self):
		count = self.userview.count()
		return count

	def get_url(self):
		url = "/polls/?type=" + str(self.p_type.slug)
		return url

class ViewPollItemsUnique(models.Model):
	p_item = models.OneToOneField(PollItem, blank=True, default=None, on_delete=models.CASCADE)
	userview = models.ManyToManyField(User, blank=True, default=None)
	vcount = models.IntegerField(default=0)#counting the number views
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.p_item)

	def get_user_count(self):
		count = self.userview.count()
		return count



class Ranking(models.Model):
	title = models.CharField(max_length=100, unique=True)
	low_score = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)
	high_score = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)
	add_days = models.IntegerField(default=0)


	def __str__(self):
		return str(self.title)



class ScorePollItemsByMonth(models.Model):
	p_item = models.ForeignKey(PollItem, on_delete=models.CASCADE)
	year = models.IntegerField(default=0)
	month = models.CharField(max_length=3)
	posi = models.IntegerField(default=0)
	nega = models.IntegerField(default=0)
	score = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.p_item)




class ScoreUserByMonth(models.Model):
	Puser = models.ForeignKey(User, on_delete=models.CASCADE)
	year = models.IntegerField(default=0)
	month = models.CharField(max_length=3)
	score = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.Puser)




class PostReport(models.Model):
	usercon = models.CharField(max_length=100)
	Puser = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
	p_item = models.ForeignKey(PollItem, on_delete=models.CASCADE)
	postissue = models.CharField(max_length=30)
	postissuemsg = models.CharField(max_length=100)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.p_item)








def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#promo analytics
class PromoAnalytic(models.Model):

    promoname = models.CharField(max_length=60, null=True, blank=False)
    promotype = models.CharField(max_length=60, null=True, blank=True)
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    promouser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='promouser',null=True , blank=False, default=None, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True) #date when the entry is created
    # active = models.BooleanField(default=True) #remove this because not needed - this is a record
    ref_id = models.CharField(max_length=6, null=True, blank=False)
 

    def __str__(self):
        return str(self.promouser)




class MarketingPromo(models.Model):

    promoname = models.CharField(max_length=60, null=True, blank=False)
    promotype = models.CharField(max_length=60, null=True, blank=True)
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE) #not neccesaary sometimes
    date = models.DateTimeField(auto_now_add=True) #date when the entry is created
    active = models.BooleanField(default=True)
    promoid = models.CharField(max_length=6, null=True, blank=False, default="None")

    def __str__(self):
        return str(self.promoname)



    def save(self, *args, **kwargs):
        # if promoid exist then check referral id if not, create a new referral id
        if self.promoid != "None":

            try:
                promocode = MarketingPromo.objects.get(promoid=self.promoid)
                #if not multipleobjects return to pass and allow for the id to be created.
                pass

            # except MarketingPromo.MultipleObjectsReturned: - had to remove this because I cant change original(none) referid pusers
            except:
                #if the id is already created to create another new id
                self.promoid = id_generator()
        else:
            self.promoid = id_generator()

        super(MarketingPromo, self).save(*args, **kwargs)



class ControlTable(models.Model):

    controlname = models.CharField(max_length=60, null=True, blank=False) 
    postadddelay = models.IntegerField(default=0) # the minutes taken before users can add new posts
    signupdays = models.IntegerField(default=0) # the number of freedays given to the users
    removepostdvotes = models.IntegerField(default=0) # the number of downvotes before a post a removed
    freedaysreferral = models.IntegerField(default=0) # the referral number of days given free to the users
    notiweekday = models.IntegerField(default=0) # the day hour weekday that sends off notification
    notihour = models.IntegerField(default=0)
    notiminute = models.IntegerField(default=0)

    delaypopsurvey = models.IntegerField(default=0)

    def __str__(self):
        return str(self.controlname)
