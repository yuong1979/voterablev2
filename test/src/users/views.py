from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView
from django.core.urlresolvers import reverse_lazy
from users.models import PUser
from django.db.models import Q
from users.forms import PUserAddForm, PUserEditForm
# from variables.models import FunctionType
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from mixins.mixins import UserChangeManagerMixin
import datetime
from polls.models import Ptype, PollItem
from django.contrib.auth.models import User
from analytics.models import ViewPollTypeUnique, ViewPollItemsUnique, Ranking
from django.db.models import Sum
from messaging.models import Message
from mixins.mixins import LoginRequiredMixin
from analytics.models import PromoAnalytic, ControlTable,MarketingPromo

class PUserDetail(DetailView):
    model = PUser
    success_url = '/puser/'
    template_name = 'PUser/user_details.html'


    def get_context_data(self, *args, **kwargs):

        context = super(PUserDetail, self).get_context_data(*args, **kwargs)

        user = self.object.user
        user = User.objects.get(id = user.id)

        context["user"] = self.object

        puser = PUser.objects.get(user=user)


        #saving the session to extract the polls created by this user
        self.request.session["user_id"] = user.id


        # Count the number polls that the user has created
        context["pollsECreated"] = PollItem.objects.filter(user_submit=user).count()


        # count the number of times users voted
        try:
            context["votedtimes"] = PollVoting.objects.filter(vote_user=user).count()
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

        # nega is a negative number so this below should be a plus
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

        #recording the user rank and points inside the PUser profile
        puser_obj = PUser.objects.get(user=user)
        puser_obj.rank = str(rk)
        puser_obj.score = pt
        puser_obj.save()








        #retrieving pollitems lists created by user
        user_obj = User.objects.get(puser=puser)
        ptype_userc = Ptype.objects.filter(pollitem__user_submit=user_obj, active=True).distinct()
        if ptype_userc:
            context["pollcreatelist"] = ptype_userc






        return context






class PUserCreate(CreateView, LoginRequiredMixin):
    model = PUser
    form_class = PUserAddForm
    # fields = ['name']
    # success_url = '/company/'
    template_name = 'PUser/create.html'
    # function = FunctionType.objects.filter(title="Employer").first()

    def dispatch(self, *args, **kwargs):
        dispatch = super(PUserCreate, self).dispatch(*args, **kwargs)

        #exit if user is not authenticated
        if not self.request.user.is_authenticated:
            return redirect('Home')

        #exit to home if puser is created and users have agreed to terms and conditions
        try:
            user = PUser.objects.get(user_id=self.request.user.id)
            # return redirect(reverse('PUserUpdate', kwargs={'pk':user.id}))
            return redirect('Home')

        except:
            pass

        return dispatch





    def form_valid(self, form):

        i = form.save(commit=False)
        i.user = self.request.user
        # i.function = self.function
        i.save()

        valid_data = super(PUserCreate, self).form_valid(form)


        ctable = ControlTable.objects.get(id=1)

        signupdays = ctable.signupdays
        referraldays = ctable.freedaysreferral

        
        try:

            referralid = form.cleaned_data['referralcode']

            #checking if the referral code is valid and inside the puser dataset
            referring_obj = PUser.objects.get(referralid=referralid)
            
            #adding freedays to the referring user dataset
            referring_obj.freedays = referring_obj.freedays + referraldays
            referring_obj.save()

            #adding freedays to the referred user dataset
            referred_obj = PUser.objects.get(user=self.request.user)
            referred_obj.freedays = referred_obj.freedays + referraldays
            referred_obj.save()

            #updating the PromoAnalytic table
            referral = PromoAnalytic.objects.get_or_create(referrer=referring_obj.user, promouser=referred_obj.user)[0]
            referral.promoname = "userreferral " + str(self.request.user)[:45]
            referral.promotype = "userreferral "
            referral.ref_id = referralid

            referral.save()

            # messages.success(self.request, "You have been given an additional " + str(referraldays) + " extra days of premium package free for using your referral code.")

        except:
            pass


        #Create a Puser        
        user = PUser.objects.get_or_create(user=self.request.user)[0]


        # on the puser account - they are not banned as default
        # on the create, update poll, create, update poll entry, if puser = banned, exit and tell user he is banned

        #add one day of free trial for complete content?
        user.freedays = user.freedays + signupdays
        user.save()



        #creating a new MarketingPromo to create the referrer promo id for the user
        newpromo = MarketingPromo.objects.get_or_create(promotype="userreferral", referrer=self.request.user)[0]
        newpromo.promoname = "userreferral " + str(self.request.user)[:45]
        newpromo.save()
        user.referralid = newpromo.promoid
        user.save() 

        # messages.success(self.request, "You have been given " + str(signupdays) + " days of premium package free trial, activate anytime.")





        return valid_data

    def get_success_url(self):
        user = self.request.user
        # obj = get_object_or_404(PUser, user=user)
        # pk = obj.pk
        # url = reverse('PUserDetail', kwargs={'pk': pk})
        messages.info(self.request, "Your profile has been created.")
        return reverse('Home')




class PUserUpdate(UserChangeManagerMixin,UpdateView): #if user is request user or staff can change
    model = PUser
    form_class = PUserEditForm
    # fields = ['name']
    # success_url = '/company/'
    template_name = 'PUser/update.html'


    def dispatch(self, *args, **kwargs):
        dispatch = super(PUserUpdate, self).dispatch(*args, **kwargs)

        #exit if user did not create poll
        if self.object.user != self.request.user:
            return redirect('Home')

        return dispatch


    def get_success_url(self):
        user = self.request.user
        obj = get_object_or_404(PUser, user=user)
        pk = obj.pk
        # url = reverse('PUserDetail', kwargs={'pk': pk})
        messages.info(self.request, "Your profile has been updated.")
        return reverse('Home')



# class PUserList(ListView):
#     model = PUser
#     template_name = 'PUser/list.html'

#     def get_queryset(self, *args, **kwargs):
#         qs = super(PUserList, self).get_queryset(**kwargs).filter()
#         query = self.request.GET.get("q")
#         if query:
#             qs = qs.filter(
#                 Q(name__icontains=query)|
#                 Q(description__icontains=query)
#                 ).order_by("-name")
#             return qs
#         else:
#             return qs




class PUserSecretList(ListView):
    model = PUser
    template_name = 'PUser/list.html'

    def get_queryset(self, *args, **kwargs):
        qs = super(PUserSecretList, self).get_queryset(**kwargs).filter()

        qs = qs.filter(trial=True)

        return qs




