from django.contrib import admin
from django import forms
from polls.models import PollItem, PollFav, Ptype, SuggestedPoll, PollVoting






class PollModelForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        fields = ('title', 'user_submit', 'description', 'score')
        model = PollItem


class PtypeAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'active', 'freepoll','locked', 'c_user', 'vote_count', 'date')
    search_fields = ['title']
    list_filter = ('active', 'freepoll','locked')

    def __str__(self,obj):
        return obj.__str__()

class PollAdmin(admin.ModelAdmin):
    list_display = ('id','title','polltype', 'allowed', 'published', 'user_submit', 'textatt', 'score', 'pollmodifydate')
    search_fields = ['title']
    forms = PollModelForm

    def __str__(self,obj):
        return obj.__str__()

class PollVotingAdmin(admin.ModelAdmin):
    list_display = ('id','vote_user','poll','vote')
    list_filter = ['vote_user']



class PollFavAdmin(admin.ModelAdmin):
    list_display = ('id','fav_user')


class SuggestedPollAdmin(admin.ModelAdmin):
    list_display = ('id', 'typePoll', 'title', 'user_submit', 'allowed', 'date', 'score')
    list_filter = ('typePoll', 'allowed')


# class SuggestVoteAdmin(admin.ModelAdmin):
#     list_display = ('id','spoll','updated','date')
    # list_display = ('id','vote_user','spoll','updated','date')


admin.site.register(Ptype, PtypeAdmin)
admin.site.register(PollItem, PollAdmin)
admin.site.register(PollVoting, PollVotingAdmin)
admin.site.register(PollFav, PollFavAdmin)

admin.site.register(SuggestedPoll, SuggestedPollAdmin)
# admin.site.register(SuggestVote, SuggestVoteAdmin)


