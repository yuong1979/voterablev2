from django.contrib import admin

# Register your models here.
from users.models import PUser


class PUserAdmin(admin.ModelAdmin):
	list_display = ['id','__str__','name','rank','score','banned','trial','subnewsletter','freedays','usermaxscore','referralid','member','memberp','alt_email','email','invoiceno','plan']

	# list_display = ['__str__','name','rank','score','banned','trial','member']

	inlines = [
	]

	# search_fields = ['user']

	search_fields = ['user__username']

	# list_filter = ('rank', 'banned')

	class Meta:
		model = PUser


	def __str__(self,obj):
		return obj.__str__()


admin.site.register(PUser, PUserAdmin)
