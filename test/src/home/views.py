from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404, HttpResponse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, View
from home.forms import ContactForm
from django.db.models import Count
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from polls.models import PollFav, PollItem, Ptype, PollVoting
from users.models import PUser
# from variables.models import Ptype
# import datetime
from datetime import datetime, timedelta
# from datetime import datetime, timedelta
import pytz
from django.core.urlresolvers import reverse
from analytics.models import ViewPollTypeUnique, ViewPollItemsUnique, Ranking, ScoreUserByMonth
from django.db.models import Sum
from variable.models import TypeYear
# from datetime import datetime, timedelta
from tags.models import TagPoll, runtagcount
import time
from django.db.models import Q
from celery.schedules import crontab
from celery.task import periodic_task
from celery import shared_task, task, app
from users.models import PUser
from messaging.models import Message
from django.views.decorators.csrf import csrf_exempt
import string
import random
from django.contrib.sessions.backends.db import SessionStore
from analytics.models import ControlTable, PromoAnalytic
from notifications.models import Notification

from tags.forms import TagSearchForm


# from django.conf import settings
# from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
# from notifications.models import Notification
# # from datetime import datetime
# import datetime
# import pytz

#Two ways to run celery tasks

# @shared_task(name='send-email-task')
# def send_email_task():
#     # testasyncemail()
#     print ("boom it works")




## For testing notifications
# http://localhost:8000/devicetoken/firebase/

# this is for email from contact form - dont touch it
@task()
def async_contact_mail(subject, contact_message, from_email, to_email):
    send_mail(
        subject=subject,
        message="",
        html_message=contact_message,
        from_email=from_email,
        recipient_list=to_email,
        fail_silently=False
    )






# testing your periodic tasks - you need to enable send email every 20secs on celery.py
@task(name='send-test-task')
def send_email_task():
    testasyncemail()
    my_date = datetime.now(pytz.timezone('Singapore'))
    time = my_date.strftime("%H:%M:%S")



## run periodic tasks on views instead of celery.py
# @periodic_task(run_every=crontab(hour=20, minute=29, day_of_week="tue"))
# def every_monday_morning():
#     #insert the tasks here
#     # testasyncemail()
#     print ("Ran successfully")





#for for the testing of sending periodic emails
def testasyncemail():

    try:
        if settings.TYPE == "base":
            from_email = settings.EMAIL_HOST_USER
        else:
            from_email = settings.DEFAULT_FROM_EMAIL
        
        my_date = datetime.now(pytz.timezone('Singapore'))
        time = my_date.strftime("%H:%M:%S")

        subject = "testing " + str(time)
        contact_message = "test message"
        form_email = "jumper23sierra@yahoo.com"
        to_email = [from_email, form_email]  # [from_email, 'jumper23sierra@yahoo.com']

        send_mail(
            subject=subject,
            message="",
            html_message=contact_message,
            from_email=from_email,
            recipient_list=to_email,
            fail_silently=False
        )
        print ("email sent!")

    except:

        print ("email failed!")
        pass







class TermsAndConditionView(TemplateView):
    template_name = "sub/termsandconditions.html"


class DisclaimerView(TemplateView):
    template_name = "sub/disclaimer.html"


class PrivacyPolicyView(TemplateView):
    template_name = "sub/privacypolicy.html"


class RefundPolicyView(TemplateView):
    template_name = "sub/refundpolicy.html"


class PromotionView(TemplateView):
    template_name = "sub/promotions.html"


class FAQView(TemplateView):
    template_name = "sub/faq.html"


class CSupportView(TemplateView):
    template_name = "sub/customer_support.html"


class TutorialsView(TemplateView):
    template_name = "sub/tutorials.html"


class AboutUsView(TemplateView):
    template_name = "sub/about.html"


class CareersView(TemplateView):
    template_name = "sub/careers.html"


class PressView(TemplateView):
    template_name = "sub/press.html"


class PartnershipsView(TemplateView):
    template_name = "sub/partnerships.html"


class SiteMapView(TemplateView):
    template_name = "sitemap.xml"


# class Logins(TemplateView):
#     template_name = "logins.html"


# class PrelimsView(TemplateView):
#     template_name = "sub/prelims.html"

# class NavView(TemplateView):
#     template_name = "navbar.html"
#     def get_context_data(self, *args, **kwargs):
#         context = super(NavView, self).get_context_data(*args, **kwargs)
#         context["form"] = SearchForm()
#         return context


class PollRedirect(TemplateView):
    template_name = "pollredirect.html"

    def dispatch(self, *args, **kwargs):
        dispatch = super(PollRedirect, self).dispatch(*args, **kwargs)
        #redirect to user create checkbox on terms and conditions not checked but user has signed in
        if self.request.user.is_authenticated:
            try: 
                test = PUser.objects.get(user_id=self.request.user.id)
            except:
                return redirect('PUserCreate')


        return dispatch




    # {% if not request.user.puser and not request.get_full_path == "/puser/add/" and not request.get_full_path == "/termsandconditions/" and not request.get_full_path == "/privacypolicy/" and not request.get_full_path == "/disclaimer/" %}


    # def get_context_data(self, *args, **kwargs):
    #     context = super(PollRedirect, self).get_context_data(*args, **kwargs)

    #     return context


# def referral(request):
#     print (request)
#     return redirect("Home")


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))






class HomeView(TemplateView, FormView):
    template_name = "home.html"
    title = 'Your Dashboard'
    form_class = TagSearchForm


    def dispatch(self, *args, **kwargs):
        dispatch = super(HomeView, self).dispatch(*args, **kwargs)
        #exit to home if user is not authenticated or exit to terms and condition agreement if user does agree
        if self.request.user.is_authenticated:
            try:
                test = PUser.objects.get(user_id=self.request.user.id)
            except:
                return redirect('PUserCreate')

        return dispatch



    def post(self, request, *args, **kwargs):
        if request.method == 'POST':

            if request.POST.get('freeday_count_id'):
                freeday_add = request.POST.get('freeday_count_id')

                #adding the number of extra days to the user subscription freeday Plus 1 to give users one full day
                # startdate = datetime.date.today()

                d = datetime.utcnow()
                startdate = pytz.utc.localize(d)

                tdelta = timedelta(days=int(freeday_add))

                enddate = startdate + tdelta

                userobj = PUser.objects.get(user=self.request.user)

                #membersubscription
                # userobj.member = True
                # userobj.substartdate = startdate
                # userobj.subenddate = enddate

                #do for memberpsubscription to give premium membership for free
                userobj.memberp = True
                userobj.substartdatep = startdate
                userobj.subenddatep = enddate


                # once the user has added the number of days to his sub reset freeday = 0
                userobj.freedays = 0
                userobj.save()

                messages.success(self.request, "You have added " + freeday_add + " days to your subscription")

                return redirect("Home")

            else:
                print ("run ajax for notifications")

                return redirect("Home")



    def get_context_data(self, *args, **kwargs):

        context = super(HomeView, self).get_context_data(*args, **kwargs)


        # http://localhost:8000/?ref=4B17MW

        #this is not working because the sessions is not working in tranferring the referralid after user login/logout
        # if self.request.GET.get("ref") == None:
        #     pass
        #     print ("skip because no referral id is used")
        # else:
        #     referralid = self.request.GET.get("ref")
        #     try:
        #         referring_obj = PUser.objects.get(referralid=referralid)
        #         self.request.session["referralid"] = referralid
        #         self.request.session.modified = True
        #         self.request.session.save()
        #         messages.success(self.request, "Your referral code allows you 3 days of additional free content when you sign up now.")

        #     except PUser.DoesNotExist:
        #         messages.success(self.request, "The referral code you used is invalid, please check.")

        #     except:
        #         print ('other errors')

        # try:
        #     print (self.request.session["referralid"])

        # except:
        #     print ('none captured')


        #update the number of tags count to only count the number of active tags
        #runtagcount needs to be everywhere because I might deactivate some polls and it needs to do a recount
        runtagcount()

        # Firebase context variables
        context['API_KEY'] = settings.API_KEY
        context['SENDER_ID'] = settings.SENDER_ID
        context['register_token'] = False


        # if user is not authenticated to display generic poll stuff
        if not self.request.user.is_authenticated:

            #######################################################################################
            ######collecting milestones tip tips and top polls  for display on landing page #######
            #######################################################################################


            # counting milestones
            countlists = Ptype.objects.filter(active=True).count()
            counttips = PollItem.objects.filter(allowed=True).count()
            counttags = TagPoll.objects.filter(active=True).count()

            context["counttips"] = counttips
            context["countlists"] = countlists
            context["counttags"] = counttags


            #collecting the top pollsters by ranking them by score
            context["pollsters"] = PUser.objects.filter().order_by('-score')[:5]

            #collecting the top polls by ranking them by score
            # context["polls"] = Ptype.objects.filter(active=True).exclude(id=1).order_by('-vote_count')[:5]

            #exclude the suggest polls and active = false
            # lister = [1,2]

            #include any polls that is either active = false or freepoll=false to be excluded later
            exclude = Ptype.objects.filter(Q(freepoll=False) | 
                               Q(active=False))

            exclude_list = exclude.values_list('pk',flat=True)

            polllist = ViewPollTypeUnique.objects.filter().exclude(p_type_id__in=exclude_list).order_by('-vcount')[:10]

            context["toppolls"] = polllist

            #collecting the top polls by ranking them by score
            context["tags"] = TagPoll.objects.filter(active=True)[:30]

        else:
            # if user is authenticated
            context['register_token'] = True
            context['userid'] = self.request.user.id

            try:
                #using a try command because the dispatch will only run after context is run and it would pop an error if puser is not created and therefore not detected

                #getting the number of days given for free if a referral is done
                ctable = ControlTable.objects.get(id=1)
                context['refdays'] = ctable.freedaysreferral

                context['refurl'] = str(self.request.user.puser.referralid)

                #pulling whether the user is subbed to the newsletter
                puserobj = PUser.objects.get(user=self.request.user)
                if puserobj.subnewsletter == True:
                    context['usernewsletter'] = "checked"
            except:
                pass

            ##################################################################
            ######collecting user favorite polls/tags and created polls#######
            ##################################################################


            #retrieving all tags from search
            searchtags = TagPoll.objects.filter(active=True)
            if searchtags:
                context["searchtags"] = searchtags


            #retrieving favourites of user
            pitem_obj = PollItem.objects.filter(pollfav__fav_user=self.request.user)
            if pitem_obj:
                #retrieving polltypes list for fav
                ptype_obj = Ptype.objects.filter(pollitem__in=pitem_obj, active=True).distinct()
                context["fav_poll_types"] = ptype_obj

            #retrieving fav tags
            fav_tags = TagPoll.objects.filter(tagfav=self.request.user, active=True)
            if fav_tags:
                context["taglist"] = fav_tags


            #retrieving pollitems lists created by user
            ptype_userc = Ptype.objects.filter(pollitem__user_submit=self.request.user, active=True).distinct()
            if ptype_userc:
                context["pollcreatelist"] = ptype_userc


            ##################################################################
            ######collecting user favorite polls/tags and created polls#######
            ##################################################################

            ######below are intensive computation, if need be, you can do a logic that computes and saves data
            ######to the database only once when user refreshes, during a 24 hour period and any subsequent refresh off home page 
            ######during the 24 hours will pull data from the database instead of computing it until the next 24 hours
            ######you will need an additional datefield in the user database to indicate when was the last time it was updated though.

            user = self.request.user


            # Count the number polls that the user has created
            context["pollsECreated"] = PollItem.objects.filter(user_submit=user).count()


            # count the number of times users voted
            try:
                context["votedtimes"] = PollVoting.objects.filter(vote_user=self.request.user).count()
            except:
                context["votedtimes"] = 0




            # extracting the count for the number of times the users have been voted up for polls and comments
            posi = PollItem.objects.filter(user_submit=user).aggregate(Sum('posi')).get('posi__sum')
            nega = PollItem.objects.filter(user_submit=user).aggregate(Sum('nega')).get('nega__sum')
            comment_likes = Message.objects.filter(senduser=user).aggregate(Sum('likes')).get('likes__sum')

            if posi is None:
                posi = 0
            if nega is None:
                nega = 0
            if comment_likes is None:
                comment_likes = 0

            pvote = (posi + nega + (comment_likes*0.2))

            context["points"] = pvote
            context["downvotes"] = nega
            context["upvotes"] = posi
            context["comment_likes"] = comment_likes





            # counting the number of users who have viewed the user created poll
            # get user created pitems
            created_items = PollItem.objects.filter(user_submit=user)
            # get list of views that belong to the pytypes created by user
            pitem_list = ViewPollItemsUnique.objects.filter(p_item__in=created_items)
            # get user created polls - you need to add distinct if you want to only count the unique no of visitors
            context["votes_poll_entries_views"] = pitem_list.values_list('userview',flat=True).count()






            ####################################################
            #overwriting the points for right now during testing
            ####################################################
            # context["points"] = 11

            #ranks the user
            pt = context["points"]

            if pt < 0:
                pt = 0

            rk = Ranking.objects.get(low_score__lte=pt, high_score__gte=pt)
            context["rank"] = rk

            #calculate next rank statistics
            next_id = rk.id + 1
            nextrk = Ranking.objects.get(id = next_id)
            #calculate the number of points to the next rank
            context["nextpts"] = int(nextrk.low_score)
            context["nextrank"] = nextrk
            context["nextfrdays"] = nextrk.add_days


            # checking if the the user has been created, if its not existing and not yet created to redirect to user create
            try:
                context["user"] = PUser.objects.get(user_id=self.request.user.id)
                #recording the user rank and points inside the PUser profile
                user = PUser.objects.get(user=self.request.user)
                user.rank = str(rk)
                user.score = pt
                user.save()
            except:
                return redirect("PUserCreate")








            # if the user is subscribed then check the date of when it ends, if today > subenddate remove membership
            d = datetime.utcnow()
            nowdate = pytz.utc.localize(d)
            membership_obj = PUser.objects.get(user=self.request.user)

            # for normal member - no longer used
            # try:
            #     dendate = PUser.objects.get(user=self.request.user).subenddate
            #     if nowdate > dendate:
            #         membership_obj.member = False
            #         membership_obj.substartdate = None
            #         membership_obj.subenddate = None
            #         membership_obj.save() 
            # except:
            #     pass

            # for premium member
            try:
                dendate = PUser.objects.get(user=self.request.user).subenddatep
                if nowdate > dendate:
                    membership_obj.memberp = False
                    membership_obj.substartdatep = None
                    membership_obj.subenddatep = None
                    membership_obj.save() 
            except:
                pass








            # counting the number of free days the user has earned
            user = PUser.objects.get(user=self.request.user)

            #ignore the adding of the freedays of usermaxscore is higher than userscore because
            #that means that the freedays has already been awarded for the current user for his score
            #usermaxscore is another name for maxlimitscore - also you can use the ranking high score that user has yet to achieve
            #update the user only once - if userscore is higher then usermaxscore - then update usermaxscore
            if user.score > user.usermaxscore:
                #update - add the number of freedays to what the user currently has and hasnt activated
                rank = Ranking.objects.get(low_score__lte=user.score, high_score__gte=user.score)
                #adding the number of days to the user
                user.freedays = user.freedays + rank.add_days
                #update the usermaxscore to to increase the maximum points the user has achieved, below this score he will not recieve freedays
                user.usermaxscore = rank.high_score
                user.save()

            if user.freedays > 0:
                context['freedays'] = user.freedays
            else:
                context['freedays'] = 0



            #  - hidden for now - consolidating and displaying the top polling users
            # context["pollsters"] = PUser.objects.all().order_by('-score')[:5]

            # exclude = Ptype.objects.filter(active=False)
            # exclude_list = exclude.values_list('pk',flat=True)
            # polllist = ViewPollTypeUnique.objects.filter().exclude(p_type_id__in=exclude_list).order_by('-vcount')[:10]
            # context["toppolls"] = polllist


        return context

















# this option to enable users to allow email notifications is unsubscribed since notifications sent by browser and not email
def SubNews(self, *args, **kwargs):

    try:

        sub = self.user.puser.subnewsletter
        if sub == True:
            subscribe = PUser.objects.get(user=self.user)
            subscribe.subnewsletter = False
            subscribe.save()
            messages.info(self, "You have now unsubscribed from Notifications")
        else:
            subscribe = PUser.objects.get(user=self.user)
            subscribe.subnewsletter = True
            subscribe.save()
            messages.info(self, "You have now subscribed to Notifications")

    except:
        messages.warning(self, "Please sign up to subscribe/unsubscribe")
        pass


    return redirect("/")



# this option to enable users to allow notifications is currently disabled
@csrf_exempt # ok to exempt no input
def api_subnews(request):

    if request.POST:
        if request.user.is_authenticated:

            urequest_id = request.POST.get('urequest_id')

            user = PUser.objects.get(user=urequest_id)

            if user.subnewsletter == False:
                user.subnewsletter = True
                user.save() 
                result = "Subscribed"
                # messages.info(request, "Subscribed!")

            else:
                user.subnewsletter = False
                user.save()
                result = "Unsubscribed"
                # messages.info(request, "Unsubscribed!")

            return JsonResponse({"result": result})
        else:
            return JsonResponse({"result": "error", "msg": "login_requred"})
    else:
        return redirect('/')

















class ContactView(FormView):
    template_name = 'contact_form.html'
    form_class = ContactForm
    success_url = '/'


    def dispatch(self, *args, **kwargs):
        dispatch = super(ContactView, self).dispatch(*args, **kwargs)
        
        #redirect to user create checkbox on terms and conditions not checked but user has signed in
        if self.request.user.is_authenticated:
            try: 
                print (PUser.objects.get(user_id=self.request.user.id))
            except:
                return redirect('PUserCreate')

        return dispatch


    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
        arguments."""

        # grab the current set of form #kwargs
        kwargs = super(ContactView, self).get_form_kwargs()
        # Update the kwargs with the user_id, so that it can be pushed as a parameter into the form
        if self.request.user.is_authenticated:
            kwargs['loggedin'] = True
        return kwargs


    def form_valid(self, form):



        if self.request.user.is_authenticated:
            # form_email = self.request.user.email

            if self.request.user.email != "":
                form_email = self.request.user.email
            else:

                if (self.request.user.puser.alt_email is not None):
                    form_email = self.request.user.puser.alt_email
                else:
                    user_id = self.request.user.puser.pk
                    messages.info(self.request, "Please update your email so we can reply you.")                    
                    return redirect(reverse('PUserUpdate', kwargs={'pk': user_id}))

            form_message = form.cleaned_data.get("message")

            form_full_name = self.request.user

        else:
            form_email = form.cleaned_data.get("email")
            form_message = form.cleaned_data.get("message")
            form_full_name = form.cleaned_data.get("full_name")
        
        subject = "Voterable Contact Form"

        if settings.TYPE == "base":
            from_email = settings.EMAIL_HOST_USER
        else:
            from_email = settings.DEFAULT_FROM_EMAIL

        to_email = [from_email, form_email]  # [from_email, 'jumper23sierra@yahoo.com']
        contact_message = "<p>Message: %s.</p><br><p>From: %s</p><p>Email: %s</p>" % (
        form_message, form_full_name, form_email)

        # include a delay behind the function that is running to run it asynchronously
        # in this case the async_contact_mail is sending a list of parameters to the sendmail function so it
        # so that asynchronously run the async_contact_mail
        try:
            async_contact_mail.delay(
                subject=subject,
                contact_message=contact_message,
                from_email=from_email,
                to_email=to_email
                )

            messages.info(self.request, "Thank you for your message, we will reply you as soon as we can.")

        except:
            messages.warning(self.request, "Error in email delivery, please send your email to hello@voterable.com")

        return super(ContactView, self).form_valid(form)




    def get_context_data(self, *args, **kwargs):
        context = super(ContactView, self).get_context_data(*args, **kwargs)
        context["submit_btn_value"] = "Send"
        return context





# #this works
# class SearchView(FormView):
#     template_name = 'base.html'
#     form_class = SearchForm
#     success_url = '/'

#     def form_valid(self, form):

#         print "test"

#         search = form.cleaned_data.get("search")

#         print search

#         messages.info(self.request, "Thank you for your message, we will reply to you soon")
#         return super(SearchView, self).form_valid(form)
 



# #this works
# class SearchView(FormView):
#     template_name = 'formtest.html'
#     form_class = SearchForm
#     success_url = '/'

#     def form_valid(self, form):

#         search = form.cleaned_data.get("search")

#         messages.info(self.request, "Thank you for your message, we will reply to you soon")
#         return super(SearchView, self).form_valid(form)
 

        # url = "/polls/?type=" + str(type_id)
        # messages.info(self.request, "Your entry has been updated.")
        # return url

# def PollSuggestion(request):
#     url = "/polls/?type=" + "suggest-your-polls"
#     return HttpResponseRedirect(url)


# def PollRecommendation(request):
#     url = "/polls/?type=" + "how-can-we-improve"
#     return HttpResponseRedirect(url)


    # return redirect("polls/?type=1")


# class Test(TemplateView):
#     # print "test1"
#     template_name = "sub/disclaimer.html"




# # We need to change this so that this will work with the latest registration
# class RegisterView(FormView):
# 	template_name = 'forms.html'
# 	form_class = RegisterForm
# 	success_url = '/'
# 	title = 'Register With Us'

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(RegisterView, self).get_context_data(*args, **kwargs)
# 		context["title"] = title
# 		context["submit_btn_value"] = "Register"
# 		return context

# 	def form_valid(self, form):
# 		username = form.cleaned_data['username']
# 		email = form.cleaned_data['email']
# 		password = form.cleaned_data['password2']
# 		# MyUser.objects.create_user(username=username, email=email, password=password)
# 		new_user = MyUser()
# 		new_user.username = username
# 		new_user.email = email
# 		new_user.set_password(password)
# 		new_user.save()
# 		#email user
# 		#create user profile instance
# 		#add message for succcess
# 		return redirect('Home')
# 		# return super(RegisterView, self).form_valid(form)


# View to serve serviceworker
class ServiceWorkerview(TemplateView):
    template_name = 'sw/serviceworker.js'
    content_type = 'application/javascript'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SENDER_ID'] = settings.SENDER_ID
        return context









