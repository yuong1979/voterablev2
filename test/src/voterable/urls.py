"""teachadvisor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from home.views import (HomeView, AboutUsView, PromotionView, ContactView, TermsAndConditionView,
    DisclaimerView, PrivacyPolicyView, RefundPolicyView, FAQView, CSupportView, TutorialsView, 
    CareersView, PressView, PartnershipsView, SiteMapView, PollRedirect, SubNews, api_subnews, ServiceWorkerview)#, SearchView


from users.views import PUserCreate, PUserUpdate, PUserDetail, PUserSecretList
from tags.views import TagView, TagAllView, api_fav, Tagsearch, TagPollsearch
# from polls.views import FavPollSub
# from polls.views import PollSearchView



from django.contrib.auth import views as auth_views
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from home.sitemaps import StaticViewSitemap, PollsSitemap, PollsTypeSitemap#, BlogSitemap
from django.views.generic import TemplateView

from billing.views import CancelSubscribe, SelectPlan, SuccessSub, ConfirmCancel, StripeCheckOut#, Subscribe1#, Subscribe0#, Subscribe2, Subscribe3, RegisterClass, StripeAddDays, StripePayment, 
from notifications.views import allin, read, readall, get_notifications_ajax, MsgCountView
from micell.views import api_survey

from analytics.views import AnalyseTags, AnalysePvote, AnalyseVid, AnalyseComplaint, RunOps, api_ops



urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # changed admin page to prevent attack
    url(r'^spiderfunky23/', admin.site.urls),

    # polling system
    url('^', include('polls.urls')),

    url(r'^accounts/', include('allauth.urls')),


    # for reference only
    # url(r"^signup/$", views.signup, name="account_signup"),
    # url(r"^login/$", views.login, name="account_login"),
    # url(r"^logout/$", views.logout, name="account_logout"),



    url(r'^$', HomeView.as_view(), name='Home'),

    # url(r'^home/$', SigninHomeView.as_view(), name='Home'),


    url(r'^analysetags/$', AnalyseTags, name='AnalyseTags'),
    url(r'^analysepvote/$', AnalysePvote, name='AnalysePvote'),
    url(r'^analysevid/$', AnalyseVid, name='AnalyseVid'),
    url(r'^analysecomplaint/$', AnalyseComplaint, name='AnalyseComplaint'),


    url(r'^runops/$', RunOps, name='RunOps'),
    url(r'^runops/success/$', api_ops, name="api_ops"),

    url(r'^contact/$', ContactView.as_view(), name='Contact'),
    url(r'^promotions/$', PromotionView.as_view(), name='Promotions'),

    url(r'^termsandconditions/$', TermsAndConditionView.as_view(), name='TermsAndCondition'),
    url(r'^disclaimer/$', DisclaimerView.as_view(), name='Disclaimer'),
    url(r'^privacypolicy/$', PrivacyPolicyView.as_view(), name='PrivacyPolicy'),
    url(r'^refundpolicy/$', RefundPolicyView.as_view(), name='RefundPolicy'),

    url(r'^FAQ/$', FAQView.as_view(), name='FAQ'),
    url(r'^customersupport/$', CSupportView.as_view(), name='Customer_Support'),
    # url(r'^tutorials/$', TutorialsView.as_view(), name='Tutorials'),puser

    url(r'^aboutus/$', AboutUsView.as_view(), name='AboutUs'),
    # url(r'^careers/$', CareersView.as_view(), name='Careers'),
    url(r'^press/$', PressView.as_view(), name='Press'),
    url(r'^partnership/$', PartnershipsView.as_view(), name='Partnership'),

    # user details
    url(r'^puser/add/$', PUserCreate.as_view(), name='PUserCreate'),
    # url(r'^puser/$', PUserList.as_view(), name='PUserList'), 
    url(r'^puser/(?P<pk>[0-9]+)/edit$', PUserUpdate.as_view(), name='PUserUpdate'),
    url(r'^puser/(?P<pk>[0-9]+)/$', PUserDetail.as_view(), name='PUserDetail'),

    # url(r'^puser/runtrialacc/$', PUserSecretList.as_view(), name='PUserSecret'),

    url(r'^tags/(?P<pk>[0-9]+)/$',  TagView.as_view(), name='TagView'),
    url(r'^tags/tsearch/', Tagsearch, name='TagSearch'),
    url(r'^tags/psearch/', TagPollsearch, name='TagPollSearch'),

    url(r'^tags/$', TagAllView.as_view(), name='TagAllView'),
    url(r'^tags/fav/$', api_fav, name="fav"),


    # url(r'^poll_suggest/$', PollSuggestion, name="PollSuggestion"),
    # url(r'^poll_recommend/$', PollRecommendation, name="PollRecommendation"),
    url(r'^poll_redirect/$', PollRedirect.as_view(), name="PollRedirect"),

    # link to send out to get people to unsub
    url(r'^suborunsub/$', SubNews, name="SubNews"),
    
    url(r'^subnews/$', api_subnews, name="subnews"),


    # http://localhost:8000/suborunsub/?

    url(r'^billing/selectplan$', SelectPlan.as_view(), name="SelectPlan"),
    url(r'^billing/subsuccess$', SuccessSub.as_view(), name="SuccessSub"),
    url(r'^billing/checkout$', StripeCheckOut.as_view(), name="StripeCheckOut"),


    #notifications
    url(r'^notifications/$', allin, name='notifications_all'),
    url(r'^notifications/ajax/$', get_notifications_ajax, name='get_notifications_ajax'),
    url(r'^notifications/(?P<id>\d+)/$', read, name='notifications_read'),
    url(r'^notifications/count/$', MsgCountView.as_view(), name='msg_count'),

    url(r'^notifications/readall$', readall, name='readall'),

    # url(r'^logins$', Logins.as_view(), name="Logins"),
    # the html for login7291 is inside test/lib/site-packages/django/contrib/auth/templates/registration
    url(r'^jumping7291/$', auth_views.login),


    # for confirming the cancellation of the users subscriptions
    url(r'^billing/cancel_subscription$', CancelSubscribe, name="CancelSubscribe"),
    url(r'^billing/confirm_cancel$', ConfirmCancel.as_view(), name="ConfirmCancel"),



    # url(r'^user/subscribesuccess$', SubscribeSuccess, name="SubscribeSuccess"),


    url(r'^survey/$', api_survey, name="survey"),


    url(r'^site-map/$', SiteMapView.as_view()),

    # seo:
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {
        'polls': PollsSitemap,
        'pollstype': PollsTypeSitemap,
        'static': StaticViewSitemap,

    }}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^robots\.txt$', TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain"
        ), name="robots_file"),

#    url(r'^test/$', SearchView.as_view(), name='SearchView'),


    # simple wysiwyg editor:
    url(r'^summernote/', include('django_summernote.urls')),



    # service worker view
    url(r'^serviceworker(.*.js)$', ServiceWorkerview.as_view() , name='service-worker'),

    # for firebasenotifications
    url(r'devicetoken/',include('firebasenotifications.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
