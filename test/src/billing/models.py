from django.db import models

# Create your models here.
from django.conf import settings






class Transaction(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)
	# beforedate = models.DateTimeField(null=True)
	# adddays = models.IntegerField(default=0)
	# afterdate = models.DateTimeField(null=True)
	transaction_id = models.CharField(max_length=120, null=False, blank=False, default="")
	# success = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	startdate = models.DateTimeField(null=True, blank=True)#paying member start date
	enddate = models.DateTimeField(null=True, blank=True)#paying member end date
	description = models.CharField(max_length=120, null=False, blank=False, default="")


	# transaction_id 
	# payment method
	# last_four

	# old
	# def __unicode__(self):
	# 	return "%s" %(self.transaction_id)

	def __str__(self):
		return str(self.transaction_id)



class PriceToDays(models.Model):
	label = models.CharField(max_length=120, null=False, blank=False, default="")
	cashprice = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)
	daystoadd = models.IntegerField(default=0)
	subplan = models.CharField(max_length=120, null=True)
	discount = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)
	active = models.BooleanField(default=False)

	def __str__(self):
		return str(self.label)






# class Transaction(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL)
# 	price = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)
# 	beforecredit = models.IntegerField(default=0)
# 	credit = models.IntegerField(default=0)
# 	aftercredit = models.IntegerField(default=0)
# 	transaction_id = models.CharField(max_length=120, null=False, blank=False, default="")
# 	success = models.BooleanField(default=True)
# 	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
# 	# transaction_id 
# 	# payment method
# 	# last_four

# 	def __unicode__(self):
# 		return "%s" %(self.transaction_id)

# class UserCredit(models.Model):
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL)
# 	credit = models.IntegerField(default=0)

# 	def __unicode__(self):
# 		return "%s" %(self.user)




# class CreditToCash(models.Model):
# 	label = models.CharField(max_length=120, null=False, blank=False, default="")
# 	cashprice = models.IntegerField(default=0)
# 	credits = models.IntegerField(default=0)
# 	discount = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)

# 	def __unicode__(self):
# 		return str(self.label)







