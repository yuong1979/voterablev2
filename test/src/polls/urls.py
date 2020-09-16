from django.conf.urls import url
from polls.views import (PollsListView, PollDetailView, api_votes, favorite_poll, #PollTopicsView,
    PollDetailCreate, PollDetailUpdate, #PollDetailDelete, PollsListFavoriteView,
    PollListCreate, PollListUpdate, PollSearchView, api_fav, api_like, api_report, api_sugglikes,
    PollSuggView, PollRecoView, PollDetailPreview, AdminPollsListView,  api_vcount
    )




urlpatterns = [
    
    # url(r'^poll_topics/$', PollTopicsView.as_view(), name="poll_topics"),


    #this should be poll list
    url(r'^polls/$', PollsListView.as_view(), name="polls_list"),

    #this is only for admin
    url(r'^adminpolls/$', AdminPollsListView, name="admin_polls_list"),


    url(r'^poll_list/add/$', PollListCreate.as_view(), name="poll_list_create"),
    url(r'^poll_list/(?P<pk>[0-9]+)/edit$', PollListUpdate.as_view(), name="poll_list_update"),
    url(r'^polls/(?P<pk>[0-9]+)/$', PollDetailView.as_view(), name="polls_detail"),
#     url(r'^polls/(?P<slug>[-\w\d]+)/$', PollDetailView.as_view(), name="polls_detail"),
    url(r'^polls/add/$', PollDetailCreate.as_view(), name='polls_detail_create'),
    url(r'^polls/(?P<pk>[0-9]+)/edit$', PollDetailUpdate.as_view(), name='polls_detail_update'),
    # url(r'^polls/(?P<pk>[0-9]+)/delete$', PollDetailDelete.as_view(), name='polls_detail_delete'),

    url(r'^polls/(?P<pk>[0-9]+)/preview$', PollDetailPreview.as_view(), name='polls_detail_preview'),


    # url(r'^polls/(?P<pk>[0-9]+)/add$', PollDetailView.as_view(), name="polls_detail"),

    # url(r'^submit_poll/$', submit_poll, name="submit_poll"),
    url(r'^polls/vote/$', api_votes, name="vote"),
    url(r'^polls/fav/$', api_fav, name="fav"),
    url(r'^polls/like/$', api_like, name="like"),
    url(r'^polls/report/$', api_report, name="report"),
    url(r'^polls/sugglikes/$', api_sugglikes, name="sugglikes"),
    url(r'^polls/vcount/$', api_vcount, name="countpviews"),

    url(r'^polls/(?P<pk>[0-9]+)/messages/add$', PollDetailView.as_view(), name="message_add"),
    url(r'^polls/(?P<pk>[0-9]+)/messages/(?P<id>[0-9]+)/edit$', PollDetailView.as_view(), name="message_edit"),

    url(r'^polls/fav_poll/(?P<pk>[0-9]+)/$', favorite_poll, name="favorite_poll"),
    
    # url(r'^polls_favorite/$', PollsListFavoriteView.as_view(), name="polls_favorite_list"),

    url(r'^polls/psearch/$', PollSearchView.as_view(), name='PollSearchView'),

    url(r'^polls/recommend/$', PollRecoView.as_view(), name='PollRecoView'),
    url(r'^polls/suggestion/$', PollSuggView.as_view(), name='PollSuggView'),
]
