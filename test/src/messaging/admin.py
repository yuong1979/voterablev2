from django.contrib import admin

# Register your models here.
from messaging.models import Message

class MessageAdmin(admin.ModelAdmin):
	list_display = ('senduser', 'pollitem', 'content', 'likes', 'timestamp', 'active')
	inlines = [
	]
	class Meta:
		model = Message

	def __str__(self,obj):
		return obj.__str__()


admin.site.register(Message, MessageAdmin)