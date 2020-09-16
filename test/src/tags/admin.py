from django.contrib import admin

# Register your models here.
from tags.models import TagPoll, TopicPoll


# class PollModelForm(forms.ModelForm):

#     class Meta:
#         fields = ('title', 'polltype', 'active', 'count')
#         model = TagPoll


# class PollAdmin(admin.ModelAdmin):
#     list_display = ('title', 'allowed', 'user_submit', 'score')
#     forms = PollModelForm


# class PollVoteAdmin(admin.ModelAdmin):
#     list_display = ('vote_user','poll')
#     forms = PollModelForm


class TopicPollAdmin(admin.ModelAdmin):
	list_display = ('title', 'active')

	def __str__(self,obj):
		return obj.__str__()

class TagPollAdmin(admin.ModelAdmin):
	list_display = ('title', 'active', 'counter')
	search_fields = ['title']
	# ordering = ('-counter',)

	def __str__(self,obj):
		return obj.__str__()

# admin.site.register(Ptype, PtypeAdmin)


admin.site.register(TagPoll, TagPollAdmin)
admin.site.register(TopicPoll, TopicPollAdmin)
# admin.site.register(PollVote, PollVoteAdmin)
# admin.site.register(PollFav)


