from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from polls.models import PollItem, PollVoting, PollFav, Ptype, SuggestedPoll
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin
from users.models import PUser
from django.contrib import messages
from django.conf import settings
# from variables.models import Ptype
from mixins.mixins import LoginRequiredMixin, UserChangeManagerMixin, PollTypeMixin
from polls.forms import PollItemAddForm, PollItemEditForm, PollItemDeleteForm, PollTopicAddForm, PollTopicEditForm, SearchForm, PollSuggAddForm, PollRecoAddForm
from django.core.urlresolvers import reverse
from tags.models import TagPoll, runtagcount
from variable.models import TypeTopic, TypeYear, TypeLocation
from analytics.models import ViewPollTypeUnique, ViewPollItemsUnique
from django.db.models import Q
from datetime import datetime, timedelta
from analytics.models import ScorePollItemsByMonth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from messaging.models import Message
from messaging.forms import PollItemMessageAddForm, PollItemMessageUpdateForm
from django.core.cache import cache
from analytics.models import PostReport
from notifications.signals import notify
import json
# import pandas as pd
from django.db.models import Q
import numpy as np
import pytz
from pytz import timezone
from django.utils.timezone import utc
# import datetime
from itertools import chain
from notifications.models import Notification
import time
from celery import shared_task, task, app
from analytics.models import ControlTable





@task()
def async_report_mail(subject, contact_message, from_email, to_email):
    send_mail(
        subject=subject,
        message="",
        html_message=contact_message,
        from_email=from_email,
        recipient_list=to_email,
        fail_silently=False
    )



###################################
######### Polltopicsfilter ########
###################################





class PollTopicsView(ListView, FormView):
    model = Ptype
    template_name = "polls/polls_types.html"
    form_class = SearchForm
    # paginate_by = 10


    # def get(self, *args, **kwargs):
    #     # if kwargs['username'] != request.user.username:
    #     #      return redirect('index')

    #     reset = "hello"
    #     if reset:
    #         return HttpResponseRedirect('?year=All&location=&poll=')

    #     return super(PollTopicsView, self).get(*args, **kwargs)


    def dispatch(self, *args, **kwargs):
        dispatch = super(PollTopicsView, self).dispatch(*args, **kwargs)
        #redirect to user create checkbox on terms and conditions not checked but user has signed in
        if self.request.user.is_authenticated:
            try: 
                test = PUser.objects.get(user_id=self.request.user.id)
            except:
                return redirect('PUserCreate')

        return dispatch


    def get_context_data(self, **kwargs):
        context = super(PollTopicsView, self).get_context_data(**kwargs)


        # if the user clicks on the the quick links from basepage it doesnt have a saved session so 
        # the cat will be not capture anything and result in error therefore specify cat as pop

        # if self.request.GET.get('cat') is None:
        #     category = self.request.session["cat"]
        # else:
        #     category = self.request.GET.get('cat')
        #     self.request.session["cat"] = category


        search = self.request.GET.get('search')

        todate = datetime.today()
        fromdate = datetime.today() - timedelta(days=365)

        if search:

            psearch = Ptype.objects.filter(Q(title__icontains=search) | 
                               Q(description__icontains=search))

            psearch = psearch.filter(active=True, date__gte=fromdate, date__lte=todate)

            # polllist = psearch.filter(active=True).exclude(id__in=[1,2]).order_by('-date')
            polllist = psearch.filter(active=True).order_by('-date')


            # if category == "Late":
            #     context['polltype'] = "Latest"
            #     polllist = psearch.filter(active=True).exclude(id__in=[1,2]).order_by('-date')

            # if category == "Vote":
            #     context['polltype'] = "Most Votes"
            #     polllist = psearch.filter(active=True).exclude(id__in=[1,2]).order_by('vote_count')

            # if category == "Pop":
            #     context['polltype'] = "Most Popular"
            #     # get top most popular for views
            #     topview_lst = ViewPollTypeUnique.objects.filter().order_by('vcount')[:50]
            #     topview_lst_id = topview_lst.values("p_type_id")
            #     polllist = psearch.filter(active=True, id__in=topview_lst_id).exclude(id__in=[1,2])

        else:

            cattype = self.request.GET.get('cattype')
            context['Cattype'] = ['Popular','Most-Votes']

            # year = self.request.GET.get('year')
            # year = TypeYear.objects.filter(title=year)

            location = self.request.GET.get('location')
            location = TypeLocation.objects.filter(title=location)

            pollcat = self.request.GET.get('poll')
            pollcat = TypeTopic.objects.filter(title=pollcat)

            Yeartype = Ptype.objects.values('year').distinct()
            context['Yeartype'] = TypeYear.objects.filter(active=True).order_by('title')

            Locationtype = Ptype.objects.values('location').distinct()
            context['Locationtype'] = TypeLocation.objects.filter(active=True).order_by('title')

            Topictype = Ptype.objects.values('topic').distinct()
            context['Topictype'] = TypeTopic.objects.filter(active=True).order_by('title')


            if cattype == "All" or not cattype:
                cattype = "Latest"



            # if year.first() is not None:
            #     year = str(year.first())

            if cattype == "Latest":
                context['polltype'] = "Latest"
                polllist = Ptype.objects.filter(active=True).order_by('-date')
                # if year and not year == "All":
                #     polllist = polllist.filter(date__year=year)
                if location and not location == "All":
                    polllist = polllist.filter(location=location)
                if pollcat and not pollcat == "All":
                    polllist = polllist.filter(topic=pollcat)

                # print (dir(polllist.first()))

            if cattype == "Most-Votes":
                context['polltype'] = "Most Votes"
                polllist = Ptype.objects.filter(active=True).order_by('vote_count')
                # if year and not year == "All":
                #     polllist = polllist.filter(date__year=year)
                if location and not location == "All":
                    polllist = polllist.filter(location=location)
                if pollcat and not pollcat == "All":
                    polllist = polllist.filter(topic=pollcat)

            if cattype == "Popular":
                context['polltype'] = "Most Popular"
                # get top most popular for views
                topview_lst = ViewPollTypeUnique.objects.filter().order_by('vcount')[:50]
                topview_lst_id = topview_lst.values("p_type_id")
                polllist = Ptype.objects.filter(active=True, id__in=topview_lst_id)
                # if year and not year == "All":
                #     polllist = polllist.filter(date__year=year)
                if location and not location == "All":
                    polllist = polllist.filter(location=location)
                if pollcat and not pollcat == "All":
                    polllist = polllist.filter(topic=pollcat)



        # numbers_list = range(1, 1000)

        polllist_list = polllist
        page = self.request.GET.get('page', 1)
        paginator = Paginator(polllist_list, 10)  # 5 - how much on one page

        try:
            polllist = paginator.page(page)
        except PageNotAnInteger:
            polllist = paginator.page(1)
        except EmptyPage:
            polllist = paginator.page(paginator.num_pages)
          
        context['polllist'] = polllist
        # this is for testing infinite pagination:
        # import time
        # time.sleep(1)


        # context['polllist'] = polllist[:50]

        return context





class PollSearchView(TemplateView):
    template_name = 'polls/polls_search.html'

    def get_context_data(self, **kwargs):
        context = super(PollSearchView, self).get_context_data(**kwargs)
        search = self.request.GET.get('search')
        # items = Ptype.objects.filter(description=search)
        items = TagPoll.objects.filter(title=search)

        context["pitems"] = items

        return context





###################################
######### Pollsuggest #############
###################################




# class PollSuggView(LoginRequiredMixin, ListView):
#     model = SuggestedPoll
#     template_name = "polls/poll_suggest_view.html"
#     paginate_by = 10
#     context_object_name = 'SuggPoll'
#     queryset = SuggestedPoll.objects.filter(allowed=True).order_by('-score')

#     def dispatch(self, *args, **kwargs):
#         dispatch = super(PollSuggView, self).dispatch(*args, **kwargs)
#         return dispatch

#     def get_queryset(self):
#         new_context = SuggestedPoll.objects.filter(allowed=True, typePoll="SG").order_by('-score')[:5]
#         return new_context

#     def get_context_data(self, **kwargs):
#         context = super(PollSuggView, self).get_context_data(**kwargs)
#         return context




#all users can suggest can suggest

class PollRecoView(LoginRequiredMixin, ListView, FormView):
    model = SuggestedPoll
    template_name = "polls/poll_recommend_view.html"
    paginate_by = 5
    context_object_name = 'RecoPoll'
    form_class = PollRecoAddForm

    # queryset = SuggestedPoll.objects.filter(allowed=True).order_by('-score')
    def dispatch(self, *args, **kwargs):
        dispatch = super(PollRecoView, self).dispatch(*args, **kwargs)
        #redirect to user create checkbox on terms and conditions not checked but user has signed in
        if self.request.user.is_authenticated:
            try: 
                test = PUser.objects.get(user_id=self.request.user.id)
            except:
                return redirect('PUserCreate')

        return dispatch



    def get_queryset(self):
        # #original
        # new_context = SuggestedPoll.objects.filter(allowed=True, typePoll="RS").order_by('-date')
        sort = self.request.GET.get('sort', None)

        #this is for shortlisting only the reccommendations from this month and ranked by votes
        d = datetime.utcnow()
        nowdate = pytz.utc.localize(d)
        enddate = nowdate - timedelta(days=90)

        if sort == "Score":
            new_context = SuggestedPoll.objects.filter(allowed=True, typePoll="RS", date__range=(enddate, nowdate)).order_by('-score')
        else:
            new_context = SuggestedPoll.objects.filter(allowed=True, typePoll="RS", date__range=(enddate, nowdate)).order_by('-date')

        return new_context

    def get_context_data(self, **kwargs):
        context = super(PollRecoView, self).get_context_data(**kwargs)
        user = self.request.user
        recolike = SuggestedPoll.objects.filter(allowed=True, typePoll="RS", vote_user=user)
        context['recolike'] = recolike
        context['form'] = self.form_class()


        context["Addpost"] = False
        #If user is staff there is no time limit
        if self.request.user.is_staff == True:
            context["Addpost"] = True

        # timing
        # check if user can post based on 1 hours after the user posted

        user = self.request.user
        # if the user has not posted anything before
        try:
        # last time the user posted
            lpostdate = SuggestedPoll.objects.filter(user_submit=user, typePoll='RS').last().date

            d = datetime.utcnow()
            nowdate = pytz.utc.localize(d)
            # okdate = lpostdate + timedelta(hours=1)
            okdate = lpostdate + timedelta(minutes=1)

            if nowdate >= okdate:
                context["Addpost"] = True
            else:
                timeleft = okdate - nowdate
                days, hours, minutes = timeleft.days, timeleft.seconds // 3600, timeleft.seconds // 60 % 60

                context["Hours"] = hours
                context["Minutes"] = minutes

        except:
            context["Addpost"] = True

        return context

    def form_valid(self, form):
        i = form.save(commit=False)
        i.typePoll = 'RS'
        i.title = form.cleaned_data.get("title")
        i.user_submit = self.request.user
        i.allowed = True
        i.save()

        valid_data = super(PollRecoView, self).form_valid(form)
        return JsonResponse('ok', safe=False)


    def form_invalid(self, form, **kwargs):
        return_dict = dict()
        e = form.errors['title'].as_text()
        return_dict['error'] = str(e)
        return JsonResponse(return_dict)


    def get_success_url(self):
        url = "/polls/recommend/"
        messages.info(self.request, "Your recommendation has been posted")
        return url








class PollSuggView(LoginRequiredMixin, ListView, FormView):
    model = SuggestedPoll
    template_name = "polls/poll_suggest_view.html"
    paginate_by = 5
    context_object_name = 'SuggPoll'
    form_class = PollSuggAddForm

    # queryset = SuggestedPoll.objects.filter(allowed=True).order_by('-score')

    def dispatch(self, *args, **kwargs):
        dispatch = super(PollSuggView, self).dispatch(*args, **kwargs)
        #redirect to user create checkbox on terms and conditions not checked but user has signed in
        if self.request.user.is_authenticated:
            try: 
                test = PUser.objects.get(user_id=self.request.user.id)
            except:
                return redirect('PUserCreate')

            if self.request.user.puser.memberp == True or self.request.user.puser.member == True:
                pass
            else:
                messages.info(self.request, "This is only for subscribers")
                return redirect('Home')

        return dispatch


    def get_queryset(self):
        # #original
        # new_context = SuggestedPoll.objects.filter(allowed=True, typePoll="SG").order_by('-date')
        sort = self.request.GET.get('sort', None)
        #this is for shortlisting only the reccommendations from this month and ranked by votes
        d = datetime.utcnow()
        nowdate = pytz.utc.localize(d)
        enddate = nowdate - timedelta(days=90)

        if sort == "Score":
            new_context = SuggestedPoll.objects.filter(allowed=True, typePoll="SG", date__range=(enddate, nowdate)).order_by('-score')
        else:
            new_context = SuggestedPoll.objects.filter(allowed=True, typePoll="SG", date__range=(enddate, nowdate)).order_by('-date')


        return new_context

    def get_context_data(self, **kwargs):
        context = super(PollSuggView, self).get_context_data(**kwargs)
        user = self.request.user
        sugglike = SuggestedPoll.objects.filter(allowed=True, typePoll="SG", vote_user=user)
        context['sugglike'] = sugglike
        context['form'] = self.form_class()

        context["Addpost"] = False
        #If user is staff there is no time limit
        if self.request.user.is_staff == True:
            context["Addpost"] = True

        # timing
        # check if user can post based on 1 hours after the user posted
        user = self.request.user
        # if the user has not posted anything before
        try:
        # last time the user posted
            lpostdate = SuggestedPoll.objects.filter(user_submit=user, typePoll='SG').last().date

            d = datetime.utcnow()
            nowdate = pytz.utc.localize(d)
            okdate = lpostdate + timedelta(hours=1)

            if nowdate >= okdate:
                context["Addpost"] = True
            else:
                timeleft = okdate - nowdate
                days, hours, minutes = timeleft.days, timeleft.seconds // 3600, timeleft.seconds // 60 % 60

                context["Hours"] = hours
                context["Minutes"] = minutes

        except:
            context["Addpost"] = True


        return context

    def form_valid(self, form):
        i = form.save(commit=False)
        i.typePoll = 'SG'
        i.title = form.cleaned_data.get("title")
        i.user_submit = self.request.user
        i.allowed = True
        i.save()

        valid_data = super(PollSuggView, self).form_valid(form)
        return JsonResponse('ok', safe=False)


    def form_invalid(self, form, **kwargs):
        return_dict = dict()
        e = form.errors['title'].as_text()
        return_dict['error'] = str(e)
        return JsonResponse(return_dict)


    def get_success_url(self):
        url = "/polls/suggestion/"
        messages.info(self.request, "Your suggestion has been posted")
        return url





@csrf_exempt # ok to exempt no input
def api_sugglikes(request):

    sugg_id =  request.POST.get('sugg_id')

    if request.POST:
        if request.user.is_authenticated:

            sugg_id =  request.POST.get('sugg_id')
            sugg_obj = SuggestedPoll.objects.filter(id=sugg_id, vote_user=request.user)

            if sugg_obj:
                # remove like
                sugg_obj.first().vote_user.remove(request.user)
                result = "unliked"
            else:
                # add like
                like = SuggestedPoll.objects.get(id=sugg_id)
                like.vote_user.add(request.user)
                result = "liked"

            try:
                sugglike_obj = SuggestedPoll.objects.get(id=sugg_id)
                sugglike_obj.sugg_score()
                likecount = sugglike_obj.score
            except:
                likecount = 0

            # return JsonResponse({"result": result})
            return JsonResponse({"result": result, "resultc": likecount })
        else:
            return JsonResponse({"result": "error", "sugglike_obj": "login_requred"})


    else:
        return redirect('/')










###################################
######### Poll lists ##############
###################################


#Polltype creation
class PollListCreate(LoginRequiredMixin, CreateView):
    model = Ptype
    form_class = PollTopicAddForm
    success_url = '/polls/'
    template_name = 'polls/polls_topic_create.html'

    def dispatch(self, *args, **kwargs):
        dispatch = super(PollListCreate, self).dispatch(*args, **kwargs)


        if self.request.user.is_authenticated:

            try: 
                test = PUser.objects.get(user_id=self.request.user.id)
            except:
                return redirect('PUserCreate')

            if self.request.user.is_staff == True:
                pass
            else:
                return redirect('/')

            #redirect user if he is banned
            user = self.request.user
            userban = PUser.objects.get(user=user)

            if userban.banned == True:
                messages.info(self.request, "You have been banned from posting, please contact us if you need help")
                return redirect('/')
        return dispatch


    # # queryset = SuggestedPoll.objects.filter(allowed=True).order_by('-score')
    # def dispatch(self, *args, **kwargs):
    #     dispatch = super(PollRecoView, self).dispatch(*args, **kwargs)
    #     #redirect to user create checkbox on terms and conditions not checked but user has signed in
    #     if self.request.user.is_authenticated:
    #         try: 
    #             test = PUser.objects.get(user_id=self.request.user.id)
    #         except:
    #             return redirect('PUserCreate')

    #     return dispatch


    def get_context_data(self, **kwargs):
        context = super(PollListCreate, self).get_context_data(**kwargs)


        return context


    def form_valid(self, form):
        i = form.save(commit=False)
        i.c_user = self.request.user
        i.active = True
        i.freepoll = True        
        i.save()

        tag_names = form.cleaned_data['tags'].split(",")
        for tag in tag_names:
            if not tag == " ":
                tag = TagPoll.objects.get_or_create(title=str(tag).strip().lower())[0]
                tag.polltype.add(i)
                tc = TagPoll.objects.get(title=tag)
                # countt = tc.polltype.count()
                # tc.counter = countt
                tc.save()

        #refresh the count of all the polls attached to a tag
        runtagcount()

        #extracting users who favorited the tag for the polllist for the poll
        userlist = TagPoll.objects.filter(polltype=i).values_list('tagfav',flat=True)
        userlist = User.objects.filter(id__in=userlist)

        action = "New Tip List"
        message = str(i)

        #creating the notifications
        for user in userlist:
            notify.send(sender=self.request.user,
                        recipient=user,
                        polltype=i,
                        pollitem=None,
                        tagpoll=None,
                        pollreview=None,
                        action=action,
                        message=message
                        )


        return super(PollListCreate, self).form_valid(form)


    def get_success_url(self):
        url = "/polls/?type=" + str(self.object.slug)
        messages.info(self.request, "Congratulations! Your poll has been created!")
        return url





class PollListUpdate(LoginRequiredMixin,UpdateView): #if user is request user or staff can change
    model = Ptype
    form_class = PollTopicEditForm
    template_name = 'polls/polls_topic_update.html'

    def dispatch(self, *args, **kwargs):
        dispatch = super(PollListUpdate, self).dispatch(*args, **kwargs)
        #exit if no poll_id
        if self.request.session.get("type_slug") == None:
            return redirect('Home')

        #exit if user did not create poll and is not a staff
        if not (self.object.c_user == self.request.user) and not (self.request.user.is_staff):
            return redirect('Home')

        return dispatch

    def get_context_data(self, **kwargs):
        context = super(PollListUpdate, self).get_context_data(**kwargs)
        return context

    def get_initial(self):
        initial = super(PollListUpdate, self).get_initial()
        #sending parameters to the form so they can be used
        tags = self.get_object().tagpoll_set.all()
        initial["tags"] = ", ".join([x.title for x in tags])
        return initial


    def form_valid(self, form):
        i = form.save(commit=False)
        i.c_user = self.request.user
        i.active = True
        i.freepoll = True
        i.save()


        tag_names = form.cleaned_data['tags'].split(",")
        obj = self.get_object()
        obj.tagpoll_set.clear()

        for tag in tag_names:
            if not tag == " ":
                tag = TagPoll.objects.get_or_create(title=str(tag).strip().lower())[0]
                tag.polltype.add(i)
                tc = TagPoll.objects.get(title=tag)
                # countt = tc.polltype.count()
                # tc.counter = countt
                tc.save()

        #refresh the count of all the polls attached to a tag
        runtagcount()

        valid_data = super(PollListUpdate, self).form_valid(form)
        return valid_data

    def get_success_url(self):
        # type_slug = self.request.session.get("type_slug")
        url = "/polls/?type=" + str(self.object.slug)
        messages.info(self.request, "Your entry has been updated.")
        return url





class PollsListView(ListView, PollTypeMixin):
    model = PollItem
    template_name = "polls/polls_list.html"
    # change paginate to control how many polls load on a page
    paginate_by = 5
    context_object_name = 'polls'
    queryset = PollItem.objects.filter(allowed=True).order_by('-score')


    def dispatch(self, *args, **kwargs):
        dispatch = super(PollsListView, self).dispatch(*args, **kwargs)
        # print (self.request.session.items())

        # to exit if this poll does not exist anymore
        if Ptype.objects.get(slug=self.request.session.get("type_slug")).active == False:
            messages.info(self.request, "This poll does not exist anymore")
            return redirect('Home')


        return dispatch


    def get_queryset(self):
        sort = self.request.GET.get('sort', None)

        poll_type = self.get_pobject().id

        ##original scripts
        # poll_type = self.get_pobject().id
        current_page = int(self.request.GET.get('page', 1))

        # to default the order of poll list by score for favorites and create
        self.order = self.request.GET.get('order_by', '-score')


        if self.request.user.is_authenticated:

            #check what type of request /favorite list/created list or general list
            if self.request.GET.get('favorite', None):
                pt_query = PollItem.objects.filter(
                                                    pollfav__fav_user=self.request.user,
                                                    polltype=poll_type
                                                    ).order_by(self.order)

            
            elif self.request.GET.get('create', None):
                pt_query = PollItem.objects.filter(
                                                    user_submit=self.request.user,
                                                    polltype=poll_type
                                                    ).order_by(self.order)


            elif self.request.GET.get('createduser', None):

                try:
                    #extracting the user id to query for the list of polls user created
                    user_id = self.request.session.get("user_id")
                    c_user = User.objects.get(id=user_id)
                except:
                    #exit back to home if the user is does not exist
                    return redirect("Home")

                pt_query = PollItem.objects.filter(
                                                    user_submit=c_user,
                                                    polltype=poll_type
                                                    ).order_by(self.order)


            else:    
                pt_query = PollItem.objects.filter()


            
            #filtering the neccessary data required by the user
            username = self.request.user.username
            # If authenticated user open first page, we get PollItems from DB and caching it
            if current_page == 1:
                if sort == "Score":
                    pt_query = pt_query.filter(allowed=True, polltype=poll_type).order_by('-score')
                    cache.set('pollitems_score'+username, pt_query)
                else:
                    pt_query = pt_query.filter(allowed=True, polltype=poll_type).order_by('-pollmodifydate')
                    cache.set('pollitems_date'+username, pt_query)

            # If authenticated user open non first page, we try get PollItems from cache
            else:
                try:
                    if sort == "Score": 
                        pt_query = cache.get('pollitems_score'+username)
                    else: 
                        pt_query = cache.get('pollitems_date'+username)
                except: # If user open non-first page directly, we get PollItems from DB and caching it
                    if sort == "Score":
                        pt_query = pt_query.filter(allowed=True, polltype=poll_type).order_by('-score')
                        cache.set('pollitems_score'+username, pt_query)
                    else:
                        pt_query = pt_query.filter(allowed=True, polltype=poll_type).order_by('-pollmodifydate')
                        cache.set('pollitems_date'+username, pt_query)
            # if users are not signed up then only restrict them to 5 entries

        else:

            #this query is for users who are not authenticated
            pt_query = PollItem.objects.filter()

            if sort == "Score":
                pt_query = pt_query.filter(allowed=True, polltype=poll_type).order_by('-score')
                # pt_query = pt_query.filter(allowed=True, polltype=poll_type).order_by('-score')[:10]
            else:
                pt_query = pt_query.filter(allowed=True, polltype=poll_type).order_by('-pollmodifydate')
                # pt_query = pt_query.filter(allowed=True, polltype=poll_type).order_by('-pollmodifydate')[:10]

        return pt_query





    def get_context_data(self, **kwargs):
        context = super(PollsListView, self).get_context_data(**kwargs)


        #check what type of request /favorite list/created list or general list
        if self.request.GET.get('favorite', None):
            context['listtitle'] = "Favorite"
            context['title'] = "Favorite List"

        elif self.request.GET.get('create', None):
            context['listtitle'] = "Created"
            context['title'] = "Created List"

        elif self.request.GET.get('createduser', None):
            context['listtitle'] = "Createduser"
            context['title'] = "User Created List"

        else:    
            context['listtitle'] = "All"
            context['title'] = "List"


        type_id = self.get_pobject().id

        # for loading polltype name and description into metatag
        context['PollType_obj'] = self.get_pobject()

        # get request session for creation or update of a new slug
        # self.request.session["type_slug"] = self.request.GET.get("type")
        self.request.session["type_slug"] = self.get_pobject().slug

        # getting the list of relevant tags/topics for the pollist
        polltype_obj = Ptype.objects.filter(id = type_id)
        tags = TagPoll.objects.filter(polltype=polltype_obj)
        context['Tags'] = tags

        # Check if this poll list is free for any user to access
        if Ptype.objects.get(id=type_id).freepoll == True:
            context['free'] = True


        context['BackPtype'] = self.get_pobject().slug

        

        # retrieve the time that the survey should pop up from the controltable to activate the survey at the alloted time
        surveypoptime = ControlTable.objects.get(id=1).delaypopsurvey
        context['surveypop'] = surveypoptime





        #only for general lists - to exclude methods for favourite and created
        if context['title'] == "List":
    
            # update the number of tips in the a polltype has inside analytics - for general poll list
            polltype = Ptype.objects.get(id=type_id)
            pollentryc = PollItem.objects.filter(allowed=True, polltype=polltype).count()
            saveentryc = ViewPollTypeUnique.objects.get_or_create(p_type_id=polltype.id)[0]
            saveentryc.ecount = pollentryc
            saveentryc.save()

            #default adding post should have time limit - If user is staff there is no time limit - for general poll list
            if self.request.user.is_staff == True:
                context["FullControl"] = True
            else:
                context["FullControl"] = False

            # check if user can post based on "cpostdelay" minutes after the user posted - for general poll list
            ctable = ControlTable.objects.get(id=1)
            cpostdelay = ctable.postadddelay
            user = self.request.user

            try:
                # search for the last time the user posted
                lpostdate = PollItem.objects.filter(user_submit=user).last().date

                d = datetime.utcnow()
                nowdate = pytz.utc.localize(d)
                okdate = lpostdate + timedelta(minutes=cpostdelay)

                if nowdate >= okdate:
                    context["Addpost"] = True
                else:
                    timeleft = okdate - nowdate
                    days, hours, minutes = timeleft.days, timeleft.seconds // 3600, timeleft.seconds // 60 % 60

                    context["Hours"] = hours
                    context["Minutes"] = minutes
            except:
                # if the user has not posted anything before
                context["Addpost"] = True


        else:

            #Create a shortcut to go to general poll list that is created/favorited (not required for general list)
            context['Go'] = self.get_pobject().slug





        if self.request.user.is_authenticated:

            # to check if user should have access to the polls
            context['userauthenticated'] = True

            #allow premium view of each poll only if user is subscribed
            if self.request.user.puser.memberp == True:
                context["Subscribedp"] = True                

            # Check if users can update the ptype - if the user is the person who created and if the polllist is not locked then authorise
            if self.request.user == Ptype.objects.get(id=type_id).c_user or self.request.user.is_staff:
                if Ptype.objects.get(id=type_id).locked == False:
                        context['user_authorised'] = True


            # retrieve the slug to redirect user to creating a new post on the slug
            context['type_slug'] = self.get_pobject().slug


            #retrieve the entries for this polltype that the users have voted for
            ptype_obj = Ptype.objects.get(id=type_id)
            user = self.request.user
            # start = time.time()
            voteposi = PollVoting.objects.filter(vote_user=user, vote=1).values_list("poll_id",flat=True)
            pollposi = PollItem.objects.filter(id__in=voteposi, polltype=ptype_obj)
            votenega = PollVoting.objects.filter(vote_user=user, vote=-1).values_list("poll_id",flat=True)
            pollnega = PollItem.objects.filter(id__in=votenega, polltype=ptype_obj)
            # end = time.time()
            # print(end - start)
            context['pollposi'] = pollposi
            context['pollnega'] = pollnega

            #not required to run for create and favourite
            #retrieve the entries that the user have favorited
            pollfav = PollFav.objects.filter(fav_user=user).values_list("poll",flat=True)
            pollfavitem = PollItem.objects.filter(id__in=pollfav, polltype=ptype_obj)
            context['PollFav'] = pollfavitem



            # #exclude entries that have been voted down more then 10 votes
            # todisallow = PollItem.objects.filter(allowed=True, polltype=ptype_obj, score__lte=-10)
            # if todisallow:

            #     for i in todisallow:
            #         # #remove all the people who favorited the disallowed post - removed as it might be confusing and take too much time
            #         # rmvfav = PollFav.objects.filter(poll=i)
            #         # if rmvfav:
            #         #     for j in rmvfav:
            #         #         j.poll.remove(i)

            #         #remove the notifications when the post is downvoted
            #         rmvnoti = Notification.objects.filter(pollitem=i)
            #         if rmvnoti:
            #             for k in rmvnoti:
            #                 k.active=False
            #                 k.save()

            #         #disallow the poll from showing on polllist
            #         i.allowed=False
            #         i.save()


            # record total number of views for the polltype on analytics table
            # only recording for users who view who is not the person who created
            if Ptype.objects.get(id=type_id).c_user != self.request.user:
                view_obj = ViewPollTypeUnique.objects.get_or_create(p_type=ptype_obj)[0]
                view_obj.userview.add(self.request.user)
                view_obj.vcount = view_obj.userview.count()
                view_obj.save()

                # #count the number of entries and save it - think about moving this to a post save so that it is less resource intensive
                # #issues here - get needs to be get_or_create if not there will be an get error - think and test consolidate this inside the below
                # pollentryc = PollItem.objects.filter(allowed=True, polltype=type_id).count()
                # saveentryc = ViewPollTypeUnique.objects.get(p_type_id=type_id)
                # saveentryc.ecount = pollentryc
                # saveentryc.save()


        return context





###################################
######### Poll detail #############
###################################

class PollDetailCreate(LoginRequiredMixin, CreateView):
    model = PollItem
    form_class = PollItemAddForm
    success_url = '/polls/'
    template_name = 'polls/polls_create.html'


    def dispatch(self, *args, **kwargs):
        dispatch = super(PollDetailCreate, self).dispatch(*args, **kwargs)
        type_id = self.request.session.get("type_id")

        #redirect user if he is banned
        if self.request.user.is_authenticated:
            user = self.request.user
            userban = PUser.objects.get(user=user)
            if userban.banned == True:
                messages.info(self.request, "You have been banned from posting, please contact us if you need help")
                return redirect('/')


        # #exit if no poll_id
        # print (self.request.session.get("type_slug"))

        if self.request.session.get("type_slug") == None:
            messages.info(self.request, "Please choose a poll to create a new entry for")
            return redirect('Home')
        return dispatch


    def get_polltype(self, *args, **kwargs):
        type_slug = self.request.POST.get("type_slug")
        # del self.request.session["type_id"]
        polltype = get_object_or_404(Ptype, slug=type_slug)   
        obj = polltype
        return obj

    def get_context_data(self, **kwargs):
        context = super(PollDetailCreate, self).get_context_data(**kwargs)
        #replaced with the below to get the right slug when add new tip is added
        # type_slug = self.request.session.get("type_slug")
        type_slug = self.request.GET.get('type_slug')
        context['type_slug'] = type_slug
        pollobj = get_object_or_404(Ptype, slug=type_slug)
        context['title'] = pollobj

        return context

    def form_valid(self, form):

        # print (dir(self.object))
        # print (dir(self.object.id))
        # print (self.object.id)

        i = form.save(commit=False)
        i.user_submit_id = self.request.user.id
        i.polltype = self.get_polltype()
        i.allowed = False

        # i.title = form.cleaned_data.get("title")
        # i.description = form.cleaned_data.get("description")
        # i.image = form.cleaned_data.get("image")
        i.save()

        valid_data = super(PollDetailCreate, self).form_valid(form)
        return valid_data

    def get_success_url(self):
        # del self.request.session["type_id"]
        # url = "/polls/?type=" + str(self.get_polltype().slug)
        # messages.info(self.request, "Your entry has been posted")

        # New - with preview
        # poll_id = self.request.session.get("poll_id")

        pk = self.object.id
        url = reverse('polls_detail_preview', kwargs={'pk': pk})

        return url





class PollDetailUpdate(LoginRequiredMixin, UpdateView): #if user is request user or staff can change
    model = PollItem
    form_class = PollItemEditForm
    template_name = 'polls/polls_update.html'

    def dispatch(self, *args, **kwargs):
        dispatch = super(PollDetailUpdate, self).dispatch(*args, **kwargs)
        # print (self.request.session.items())

        #exit if no poll_id
        if self.request.session.get("poll_id") == None:
            messages.info(self.request, "Please choose a poll to update")
            return redirect('Home')

        #exit if user did not create poll and is not a staff
        if not (self.object.user_submit == self.request.user) and not (self.request.user.is_staff):
            return redirect('Home')

        return dispatch

    def get_context_data(self, **kwargs):
        context = super(PollDetailUpdate, self).get_context_data(**kwargs)
        # pollobj = get_object_or_404(Ptype, slug=type_slug)
        #save the session id so this submission is directed to the right preview
        self.request.session["poll_id"] = self.get_object().id
        context['title'] = self.object.title

        # messages.info(self.request, "Please note that once you update you will lose comments and points for this entry")
        return context

    def form_valid(self, form):

        my_date = datetime.now(pytz.timezone('Singapore'))
        poll_obj = self.object
        poll_obj.pollmodifydate = my_date
        poll_obj.save()

        # user = self.request.user
        # form.instance.user = user

        # if (self.object.title == form.instance.title) and (self.object.description == form.instance.description) and (self.object.image == form.instance.image) and (self.object.imageurl == form.instance.imageurl):
        #     pass
        # else:
        #     print ("run clean function - lose comments and points for this entry")

        # print (self.object.title)
        # print (self.object.description)
        # print (self.object.image)
        # print (self.object.imageurl)

        # print (form.instance.title)
        # print (form.instance.description)
        # print (form.instance.image)
        # print (form.instance.imageurl)

        valid_data = super(PollDetailUpdate, self).form_valid(form)
        return valid_data

    def get_success_url(self):
        # Original - no preview
        # poll_id = self.request.session.get("poll_id")
        # pk = poll_id
        # url = reverse('polls_detail', kwargs={'pk': pk})
        # messages.info(self.request, "Your entry has been updated.")

        # New - with preview
        poll_id = self.request.session.get("poll_id")
        pk = poll_id
        url = reverse('polls_detail_preview', kwargs={'pk': pk})
        return url



class PollDetailPreview(LoginRequiredMixin, TemplateView):
    template_name = 'polls/polls_detail_preview.html'


    def dispatch(self, *args, **kwargs):
        dispatch = super(PollDetailPreview, self).dispatch(*args, **kwargs)
        PollItem_id = self.kwargs.get('pk')
        Poll = PollItem.objects.get(pk=PollItem_id)

        #exit if user did not create poll and is not a staff
        if not (Poll.user_submit == self.request.user) and not (self.request.user.is_staff):
            return redirect('Home')

        return dispatch

    def get_context_data(self, **kwargs):
        context = super(PollDetailPreview, self).get_context_data(**kwargs)
        pollobj_id = self.kwargs.get('pk')
        pollobj = PollItem.objects.get(pk=pollobj_id)
        ptypeobj = pollobj.polltype

        context['poll'] = pollobj
        context['pt'] = ptypeobj
        context['Back'] = pollobj_id

        return context

    def post(self, request, *args, **kwargs):
        pollobj_id = self.kwargs.get('pk')

        if request.method == 'POST':

            #when user confirms the post will be published 
            if request.POST.get('pub_poll_id') is not None:
                poll_id_pub = request.POST.get('pub_poll_id')

                pitem_obj = PollItem.objects.get(pk=pollobj_id)
                pitem_obj.allowed = True
                pitem_obj.save()

                # #update the number of tips in the a polltype has inside analytics
                ptypeobj = pitem_obj.polltype

                #notifications to update users - originally time was used to alert users
                # d = datetime.utcnow()
                # nowdate = pytz.utc.localize(d)
                # publishdate = pitem_obj.date + timedelta(minutes=1)

                #extracting users who favorited the poll under polllist
                pitemreq = PollItem.objects.filter(polltype=ptypeobj)
                userlist0 = PollFav.objects.filter(poll__in=pitemreq).values_list('fav_user',flat=True).distinct()

                #extracting users who favorited the tag for the polllist for the poll
                userlist1 = TagPoll.objects.filter(polltype=ptypeobj).values_list('tagfav',flat=True)

                # set is for distinct list, chain is for combining querysets into a list
                result_list = list(set(chain(userlist0, userlist1)))
                userlist = User.objects.filter(id__in=result_list)


                if not Notification.objects.filter(pollitem=pitem_obj, action="New Tip"):
                    # create new tip because new tip for this item does not currently exist
                    #message to the user
                    message = str(pitem_obj)

                    action = "New Tip"

                    for i in userlist:
                        notify.send(sender=self.request.user,
                                    recipient=i,
                                    polltype=ptypeobj,
                                    pollitem=pitem_obj,
                                    tagpoll=None,
                                    pollreview=None,
                                    action=action,
                                    message=message
                                    )


                messages.info(self.request, "Your post has been published")

                return HttpResponseRedirect(reverse('polls_detail', kwargs={'pk': pollobj_id}))









# AdminPollsListView

def AdminPollsListView(request):
    pslug = request.GET.get('type') 
    ptype_obj = Ptype.objects.filter(slug=pslug)
    polllist = PollItem.objects.filter(polltype=ptype_obj).order_by('-date')

    context = {
                'polls': polllist, 
                }
                
    return render(request, 'polls/admin_poll_list.html', context)






# class PollDetailDelete(LoginRequiredMixin,UpdateView): #if user is request user or staff can change
#     model = PollItem
#     form_class = PollItemDeleteForm
#     template_name = 'polls/polls_disallow.html'

#     def dispatch(self, *args, **kwargs):
#         dispatch = super(PollDetailDelete, self).dispatch(*args, **kwargs)

#         if self.request.session.get("poll_id") == None:
#             messages.info(self.request, "Please choose a poll to delete")
#             return redirect('Home')

#         return dispatch

#     # def get_context_data(self, **kwargs):
#     #     context = super(PollDetailDelete, self).get_context_data(**kwargs)
#     #     poll_id = self.request.session.get("poll_id")
#     #     context['poll_id'] = poll_id
#     #     return context

#     def form_valid(self, form):
#         self.object.allowed = False
#         self.object.save()
#         valid_data = super(PollDetailDelete, self).form_valid(form)
#         return valid_data

#     def get_success_url(self):
#         # url = "/"
#         type_slug = self.request.session.get("type_slug")
#         url = "/polls/?type=" + str(type_slug)
#         messages.info(self.request, "Your entry has been deleted.")
#         return url









class PollDetailView(LoginRequiredMixin, DetailView, FormView):
    model = PollItem
    context_object_name = 'poll'
    template_name = "polls/polls_detail.html"
    form_class = PollItemMessageAddForm
    second_form_class = PollItemMessageUpdateForm


    def dispatch(self, *args, **kwargs):
        dispatch = super(PollDetailView, self).dispatch(*args, **kwargs)
        if self.get_object().allowed != True:
            messages.info(self.request, "This is item is no longer available")
            return redirect('Home')

        # send the user to premium subscribe if the user wants to access details unless he is member or he created this entry
        try:
            if (self.object.user_submit != self.request.user) and (self.request.user.puser.memberp == False) and (self.object.polltype.freepoll != True):
                messages.info(self.request, "Please subscribe to the premium package plan to access details")
                return redirect('SelectPlan')
        except:
            pass

        return dispatch


    def get_context_data(self, *args, **kwargs):

        context = super(PollDetailView, self).get_context_data(**kwargs)
        context['listtitle'] = "Detail"


        if self.request.user.is_authenticated:


            obj = self.get_object()
            msgobj = Message.objects.filter(senduser=self.request.user, pollitem=obj).first()

            # Check if this ptype is free
            if obj.polltype.freepoll == True:
                context['free'] = True

            # backward to the polltype from the poll tip
            context['BackPtype'] = obj.polltype.slug

            # if msgobj:
            #     INITIAL_DATA = {'content': msgobj.content}

            # two form classes are created one for update and one for create comments
            if msgobj:
                context['form'] = self.second_form_class(request=self.request, initial={'content': msgobj.content})
            else:
                context['form'] = self.form_class(request=self.request)
                

            context["user"] = PUser.objects.get(user=self.request.user)

            pollitem_obj = PollItem.objects.get(id=self.object.id)
            # is it favorited by current user?    
            # context["Submit"] = "Favorite"
            # if PollFav.objects.filter(fav_user=self.request.user, poll=pollitem_obj):
            #     context["Submit"] = "Unfavorite"

            if self.object.user_submit != self.request.user:
                view_obj = ViewPollItemsUnique.objects.get_or_create(p_item=self.object)[0]
                view_obj.userview.add(self.request.user)
                view_obj.vcount = view_obj.userview.count()
                view_obj.save()



        # getting the number of views
        try:
            view_obj = ViewPollItemsUnique.objects.get(p_item=self.object)
            context['Views'] = view_obj.vcount
        except:
            pass


        # getting the number of favorites
        try:
            fav_obj = PollFav.objects.filter(poll=self.object)
            context['Favorited'] = fav_obj.count()

        except:
            pass


        ## getting the analytics
        # try:
        #     todate = datetime.now(tzinfo=pytz.UTC)
        #     # todate = datetime.datetime.now()
        #     fromdate = todate - timedelta(days=365)

        #     # context['Analytics'] = ScorePollItemsByMonth.objects.filter(p_item=self.object, updated__gte=fromdate, updated__lte=todate)

        #     # sort the querydata by id
        #     df = ScorePollItemsByMonth.objects.filter(p_item=self.object, updated__range=[fromdate, todate]).order_by('id')

        #     df = df.values_list('year','month','posi','nega', flat=False)
        #     #inserting the collected data into a dateframe for manipulation
        #     df = pd.DataFrame(list(df))
        #     #giving the dataframe column names
        #     df.columns = ['year','month','posi','nega']
        #     #concatenate the period
        #     df["period"] = df["year"].map(str) + "-" + df["month"]
        #     #reverse the negative sign
        #     df["nega"] = df["nega"]*-1
        #     df = df[['period','posi','nega']]
        #     #changing column names
        #     df.rename(columns={'posi':'Upvotes','nega':'Downvotes'}, inplace=True)
        #     #adding the header to a list format
        #     dfcolumn = [df.columns.values.tolist()]
        #     #adding the values to a list format
        #     df = df.values.tolist()
        #     #adding both together
        #     df = dfcolumn + df

        #     context["datav"] = json.dumps(df)

        # except:
        #     pass





        # get user details
        context['Userdetail'] = PUser.objects.get(user=self.object.user_submit).get_absolute_url()

        # getting the poll messages related to this pollitem

        sort = self.request.GET.get('sort', None)
        poll_type = self.request.GET.get('type', None)


        if sort == "Date":
            context["msg"] = Message.objects.filter(pollitem=self.get_object()).order_by('updated')
        else:
            context["msg"] = Message.objects.filter(pollitem=self.get_object()).order_by('-likes')
            

        # saving the poll id for updates and adding
        self.request.session["poll_id"] = self.get_object().id


        if self.request.user.is_authenticated:

            #check if the user is the creator of the poll if so offer the option to update
            if (self.request.user == self.get_object().user_submit) or (self.request.user.is_staff):
                context['user_authorised'] = True

            if self.request.user.is_staff == True:
                context['user_staff'] = True


            if PollFav.objects.filter(fav_user=self.request.user, poll=self.get_object()).exists():
                context['favorited'] = True
            else:
                context['favorited'] = False


            user = self.request.user
            msglike = Message.objects.filter(userlikes=user,pollitem=self.get_object())
            context['msglike'] = msglike


            #allow basic view of each poll only of user is subscribed
            # if self.request.user.puser.member == True:
            #     context["Subscribed"] = True

            #allow premium view of each poll only of user is subscribed
            if self.request.user.puser.memberp == True:
                context["Subscribedp"] = True      


        return context




    def form_valid(self, form):

        Msgobj = Message.objects.get_or_create(senduser=self.request.user, pollitem=self.get_object())[0]
        #clear all likes
        Msgobj.userlikes.clear()
        #reset all likes in model
        Msgobj.calc_likes()

        Msgobj.content = form.cleaned_data.get("content")
        Msgobj.save()

        #retrieving the pollitem
        rcontent = Message.objects.get(id=Msgobj.id).content
        #retrieving the pollitem
        pitemreq = Message.objects.get(id=Msgobj.id).pollitem
        #retrieving the user who submitted the poll
        user_submit = pitemreq.user_submit
        #inserting the message into notifications
        message = str(rcontent)


        # check if new is already existing
        try:
            existing_new = Notification.objects.get(pollitem=pitemreq, action="New Review", recipient=user_submit, sender=self.request.user)

        except:
            existing_new = None

        # check if updated is already existing
        try:
            existing_updated = Notification.objects.get(pollitem=pitemreq, action="Updated Review", recipient=user_submit, sender=self.request.user)

        except:
            existing_updated = None


        #updated notifications
        if existing_new:
            # if a review exist already change it to updated review and read = false
            existing_new.action = "Updated Review"
            existing_new.read = False
            existing_new.message = message
            existing_new.save()

        elif existing_updated:
            # if a review is already updated then just change read = false
            existing_updated.read = False
            existing_updated.message = message
            existing_updated.save()

        else:
            # if reviews do not currently exist for the user to the user created then just create a new review
            action = "New Review"

            notify.send(sender=self.request.user,
                        recipient=user_submit,
                        polltype=None,
                        pollitem=pitemreq,
                        tagpoll=None,
                        pollreview=None,
                        action=action,
                        message=message
                        )

        valid_data = super(PollDetailView, self).form_valid(form)
        return valid_data


    def form_invalid(self, form, **kwargs):

        #refresh the context?

        return render(self.request, self.template_name, {'errors': form.errors, 'form':form})


    def get_success_url(self):
#         url = "/polls/" + self.slug
        url = "/polls/" + str(self.get_object().id)
        messages.info(self.request, "Your comment has been posted")
        return url











# def submit_poll(request):

#     if request.POST:
#         order_by = request.POST.get('order_by', '-score')
#         polltype = request.POST.get('poll_type')
#         title = request.POST.get('poll_title')
#         # image = request.POST.get('image', None)
#         try:
#             image = request.FILES['image']
#         except KeyError:
#             image = None
#         description = request.POST.get('poll_description')
#         PollItem.objects.create(title=title,
#                                 image=image,
#                                 description=description,
#                                 user_submit=request.user,
#                                 polltype_id=int(polltype))
#         return redirect("/polls/?sent=true&type=" + polltype + "&order_by=" + order_by)
#     else:
#         return redirect("/")






# this us using a form to so that data is send to the back end to check for xxs/sql injection
from django import forms

class reportForm(forms.Form):
    poll_id = forms.IntegerField()
    issue_id = forms.CharField()
    issuemsg = forms.CharField()




# reporting a poll does not remove the poll - it emails the admin and admin will decide to remove the poll
def api_report(request):

    if request.POST:

        if request.user.is_authenticated:

            form = reportForm(request.POST)

            if form.is_valid():

                #redirect user if he is banned
                user = request.user
                userban = PUser.objects.get(user=user)
                if userban.banned == True:
                    messages.info(request, "You have been banned from posting, please contact us if you need help")
                    return redirect('/')

                pollid =  form.cleaned_data.get('poll_id')
                issueid =  form.cleaned_data.get('issue_id')
                issuemsg =  form.cleaned_data.get('issuemsg')

                result = pollid


                # gathering email form data for emailing to myself
                subject = "Voterable Report Form"

                if settings.TYPE == "base":
                    from_email = settings.EMAIL_HOST_USER
                else:
                    from_email = settings.DEFAULT_FROM_EMAIL

                try:
                    form_email = request.user.email
                    to_email = [from_email, form_email]  # [from_email, 'jumper23sierra@yahoo.com']
                except:
                    form_email = None
                    to_email = [from_email]  # [from_email, 'jumper23sierra@yahoo.com']

                contact_message = "Poll item " + str(pollid) + " has been reported for " + issueid + " by user " + str(request.user.id)


                #updating the report database with the issue the request has
                try:
                    if (request.user.puser.alt_email is not None) and (request.user.puser.alt_email != ""):
                        useremail = request.user.puser.alt_email
                    elif (request.user.puser.email is not None) and (request.user.puser.email != ""):
                        useremail = request.user.puser.email
                    elif (request.user.email is not None) and (request.user.email != ""):
                        useremail = request.user.email
                    else:
                        useremail = "Anonymous"
                except:
                    useremail = "Anonymous"

                pollobj = get_object_or_404(PollItem, id=pollid)

                #user cannot vote for a post that he has created
                if pollobj.user_submit == user:
                    return redirect('/')
                else:
                    pass

                # if the user has reported already then just get and replace the latest issue in the database
                # We save the issuemsg model field only if we don't get 'true' from our frontend
                preport = PostReport.objects.get_or_create(p_item=pollobj, Puser=request.user)[0]

                
                if issuemsg != 'true':
                    preport.postissuemsg = issuemsg
                preport.usercon = useremail
                preport.postissue = issueid
                preport.save()


                # original email send without async
                send_mail(
                    subject=subject,
                    message="Poll item " + str(pollid) + " has been reported for issue " + issueid,
                    html_message=contact_message,
                    from_email=from_email,
                    recipient_list=to_email,
                    fail_silently=False
                )

                # # emailing the report to myself so I can make a decision to hide/disallow the poll as admin
                # async_report_mail.delay(
                #     subject=subject,
                #     contact_message=contact_message,
                #     from_email=from_email,
                #     to_email=to_email
                #     )
            
            return JsonResponse({"result": result })

        else:
            return redirect('/')





#counting the number of views when a poll has when dropdown is clicked on
@csrf_exempt # ok to exempt no input
def api_vcount(request):

    if request.POST:
        if request.user.is_authenticated:
            poll_id = request.POST.get('poll_id')

            pobj = PollItem.objects.get(id=poll_id)

            if pobj.user_submit != request.user:
                view_obj = ViewPollItemsUnique.objects.get_or_create(p_item=pobj)[0]
                view_obj.userview.add(request.user)
                view_obj.vcount = view_obj.userview.count()
                view_obj.save()

            result = "success"

            return JsonResponse({"result": result})
        else:
            return JsonResponse({"result": "error", "msg": "login_requred"})
    else:
        return redirect('/')




@csrf_exempt # ok to exempt no input
def api_like(request):
    # msg_id =  request.POST.get('msg_id')

    if request.POST:
        if request.user.is_authenticated:

            msg_id =  request.POST.get('msg_id')
            # poll_id =  request.POST.get('poll_id')
            # pollitem_obj = PollItem.objects.get(id=poll_id)

            # exit if the user who liked it is the same as the user who posted the message
            poll_submit_user = Message.objects.get(id=msg_id).senduser
            if poll_submit_user == request.user:
                return redirect('/')


            msg_obj = Message.objects.filter(id=msg_id, userlikes=request.user)

            if msg_obj:
                # remove like
                msg_obj.first().userlikes.remove(request.user)
                result = "unliked"
            else:
                # add like
                like = Message.objects.get(id=msg_id)
                like.userlikes.add(request.user)
                result = "liked"

            try:
                msg = Message.objects.get(id=msg_id)
                msg.calc_likes()
                likecount = msg.likes
            except:
                likecount = 0

            # return JsonResponse({"result": result})
            return JsonResponse({"result": result, "resultc": likecount })
        else:
            return JsonResponse({"result": "error", "msg": "login_requred"})
    else:
        return redirect('/')




@csrf_exempt # ok to exempt no input
def api_fav(request):

    if request.POST:
        if request.user.is_authenticated:
            poll_id =  request.POST.get('poll_id')
            pollitem_obj = PollItem.objects.get(id=poll_id)
            poll_fav = PollFav.objects.filter(poll=pollitem_obj, fav_user=request.user)

            if poll_fav:
                # remove favorite
                poll_fav.first().poll.remove(pollitem_obj)
                result = "unfavorited"
                # messages.info(request, "Unfavorited!")

            else:
                # add favorite
                fav = PollFav.objects.get_or_create(fav_user=request.user)[0]
                fav.save()
                fav.poll.add(pollitem_obj)
                result = "favorited"
                # messages.info(request, "Favorited!")

            return JsonResponse({"result": result})
        else:
            return JsonResponse({"result": "error", "msg": "login_requred"})
    else:
        return redirect('/')


# this is no longer being used
# add poll to favorite:
def favorite_poll(request, pk):
    pollitem_obj = PollItem.objects.get(id=pk)
    poll_fav = PollFav.objects.filter(poll=pollitem_obj, fav_user=request.user)

    if poll_fav:
        # remove favorite
        poll_fav.first().poll.remove(pollitem_obj)
        messages.info(request, "Unfavorited!")

    else:
        # add favorite
        fav = PollFav.objects.get_or_create(fav_user=request.user)[0]
        fav.save()
        fav.poll.add(pollitem_obj)
        messages.info(request, "Favorited!")

    favorite = request.POST.get("favorite", None)
    if favorite:
        return redirect('/polls/favorite_list/?favorite=' + favorite)
    else:
        return redirect('/polls/' + str(pk))


@csrf_exempt # ok to exempt no input
def api_votes(request):

    if request.POST:

        if request.user.is_authenticated:

            # #if no longer the same year implement this in the new year to close off the year
            # todateyear = datetime.today().year
            # type_id = request.session.get("type_id")
            # pollyear = get_object_or_404(Ptype, id=type_id).year
            # if str(todateyear) != str(pollyear):
            #     messages.info(request, "The voting for this poll has ended")

            #redirect user if he is banned
            user = request.user
            userban = PUser.objects.get(user=user)
            if userban.banned == True:
                messages.info(request, "You have been banned from posting, please contact us if you need help")
                return redirect('/')

            poll_id = request.POST.get('poll_id')
            poll = PollItem.objects.get(id=poll_id)

            if poll.user_submit == user:
                #user cannot vote for a post that he has created
                return redirect('/')
            else:
                pass

            #updating the vote count for the poll
            vote_obj = PollVoting.objects.get_or_create(vote_user=request.user, poll=poll)[0]

            if request.POST.get('posi') == "true":
                if vote_obj.vote == 1:
                    vote_obj.vote = 0
                else:
                    vote_obj.vote = 1

            if request.POST.get('nega') == "true":
                if vote_obj.vote == -1:
                    vote_obj.vote = 0
                else:
                    vote_obj.vote = -1

                    #exclude poll entries that have been voted down more the number of votes stipulated in the database
                    print (poll.score)

                    #check the number of downvotes a poll should get before removal
                    ctable = ControlTable.objects.get(id=1)
                    rmvotesno = ctable.removepostdvotes

                    #poll disallowed or removed
                    if poll.score <= -rmvotesno:
                        poll.allowed=False
                        poll.save()

                        #remove the notifications (if any) for the poll after it had been removed
                        rmvnoti = Notification.objects.filter(pollitem=poll)
                        if rmvnoti:
                            for k in rmvnoti:
                                k.active=False
                                k.save()



            vote_obj.save()

            #refresh the score of the poll in the database
            poll.calc_score()

            #include the below if you need to vote numbers back to the user
            return JsonResponse({"result": poll.score, "resultvote": vote_obj.vote, "pvote": poll.posi})
            # return JsonResponse({"result": poll.score})

        else:
            return JsonResponse({"result": "error", "msg": "login_requred"})
    else:
        return redirect('/')






