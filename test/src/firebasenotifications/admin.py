from django.contrib import admin

# Register your models here.
from firebasenotifications.models import DeviceToken


class DeviceTokenAdmin(admin.ModelAdmin):
	# list_display = ['__str__','user_id','device_token','created']
	list_display = ['__str__','userdt','user_id','device_token','created']

	# inlines = [
	# ]

	search_fields = ['user_id']

	# search_fields = ['user__username']
	# list_filter = ('created','user_id')

	class Meta:
		model = DeviceToken


	def __str__(self,obj):
		return obj.__str__()


admin.site.register(DeviceToken, DeviceTokenAdmin)
