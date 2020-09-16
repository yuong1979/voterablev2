from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class DeviceToken(models.Model):

	userdt = models.ForeignKey(User,default=None, on_delete=models.CASCADE)
	user_id = models.IntegerField()
	device_token = models.CharField(max_length=300, unique=True)
	created = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('created',)
