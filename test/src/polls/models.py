from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from variable.models import TypeTopic, TypeLocation, TypeYear
# from analytics.models import models
from django.apps import apps
# from variables.models import Ptype
from django.db.models import Sum
from markdown_deux import markdown
from django.conf import settings
from django import template
register = template.Library()
from django.template.defaultfilters import slugify
import shutil


def ptype_image_upload_to(instance, filename):
    ptype_id = instance.id
    # teacher_id = instance.id
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(basename, ptype_id, file_extension)
    olddir = "%s/ptype/%s/img" %(settings.MEDIA_ROOT, ptype_id)
    shutil.rmtree(olddir, ignore_errors=True)
    return "ptype/%s/img/%s" %(ptype_id, new_filename)


class Ptype(models.Model):
    c_user = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=100, unique=True)

    year = models.ForeignKey(TypeYear, on_delete=models.PROTECT, null=True, blank=True)
    location = models.ForeignKey(TypeLocation, on_delete=models.PROTECT, null=True, blank=True)
    topic = models.ForeignKey(TypeTopic, on_delete=models.PROTECT, null=True, blank=True)

    subtopic = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(null=True, blank=False, unique=True)
    image = models.ImageField(blank=True, null=True, upload_to=ptype_image_upload_to, max_length=2048)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True) #date when the entry is created

    freepoll = models.BooleanField(default=False)

    vote_count = models.IntegerField(default=0)
    locked = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=150, null=True, blank=True, allow_unicode=True)
    
    # #Override models save method to store slug field:
    # def save(self, *args, **kwargs):
    #     print ("testing")
    #     super(Ptype, self).save(*args, **kwargs)
    #     #Only set the slug when the object is created.
       
    #     if self.id:
    #         self.slug = slugify(self.title) #Or whatever you want the slug to use 
    #         super(Ptype, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    def get_update(self):
        return reverse('poll_list_update', kwargs={'pk': self.pk})

    #this does not work because of the slug - instead use the one below
    # def get_absolute_url(self):
    #     return reverse("polls_list", kwargs={"pk":self.pk})

    def get_url(self):
        url = "/polls/?type=" + str(self.slug)
        return url

    # def get_entry_count(self):
        # count = self.vote_count
        # print (count)
        # return count


def pitem_image_upload_to(instance, filename):
    pitem_id = instance.id
    # teacher_id = instance.id
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(basename, pitem_id, file_extension)
    olddir = "%s/pitem/%s/img" %(settings.MEDIA_ROOT, pitem_id)
    shutil.rmtree(olddir, ignore_errors=True)
    return "pitem/%s/img/%s" %(pitem_id, new_filename)


class PollItem(models.Model):
    polltype = models.ForeignKey(Ptype, on_delete=models.PROTECT, blank=True, null=True, default=None)
    title = models.CharField(max_length=100, unique=False)

    image = models.ImageField(blank=True, null=True, upload_to=pitem_image_upload_to, max_length=2048)
    imageurl = models.URLField(max_length=200, null=True, blank=True)
    imgatt = models.CharField(max_length=100, unique=False, null=True, blank=True)

    user_submit = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=False, unique=True)
    textatt = models.CharField(max_length=100, unique=False, null=True, blank=True)
    # text_html = models.TextField(editable=False) # don't want to see this in Admin

    url = models.URLField(max_length=200, null=True, blank=True)
    

    ytubeurl = models.URLField(max_length=200, null=True, blank=True) #maybe adding youtube
    fburl = models.URLField(max_length=200, null=True, blank=True) #maybe adding facebook
    googurl = models.URLField(max_length=200, null=True, blank=True) #maybe adding google
    yelpurl = models.URLField(max_length=200, null=True, blank=True) #maybe adding yelp
    amzurl = models.URLField(max_length=200, null=True, blank=True) #maybe adding amazon

    # allowed = models.BooleanField(default=False, choices=allowed_choices)
    published = models.BooleanField(default=False)
    allowed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True) #date when the entry is created
    # adding the modified datetimefield for the poll in case it needs to be sorted by if any entry was modified
    modifieddate = models.DateTimeField(auto_now=True) #last modified timestamp
    score = models.IntegerField(default=0)
    posi = models.IntegerField(default=0)
    nega = models.IntegerField(default=0)

    pollmodifydate = models.DateTimeField(auto_now_add=True, blank=False, null=True) #last modified timestamp

#     slug = models.SlugField(unique=True, max_length=150, null=True, blank=True)

    # def save(self, force_insert=False, force_update=False):
    #     self.text_html = markdown(self.text)
    #     return super(PollItem, self).save(self, *args, **kwargs)
    
    #Override models save method to store slug field:
#     def save(self, *args, **kwargs):
#         super(PollItem, self).save(*args, **kwargs)
#         #Only set the slug when the object is created.
#        
#         if self.id:
#             self.slug = slugify(self.title) #Or whatever you want the slug to use 
#             super(PollItem, self).save(*args, **kwargs)


    def get_update(self):
        return reverse('polls_detail_update', kwargs={'pk': self.pk})

    # def get_delete(self):
    #     return reverse('polls_detail_delete', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse("polls_detail", kwargs={"pk":self.pk})


    # def calc_score(self):
    #     pvotes = PollVote.objects.filter(poll=self, posi=True).count()
    #     self.posi = pvotes
    #     nvotes = PollVote.objects.filter(poll=self, nega=True).count()
    #     self.nega = nvotes
    #     score = pvotes - nvotes
    #     self.score = score
    #     #add allowed = False if the score goes below a certain number
    #     self.save()


    def calc_score(self):

        votes = PollVoting.objects.filter(poll=self).aggregate(Sum('vote')).get('vote__sum')
        if votes is None:
            votes = 0

        pvotes = PollVoting.objects.filter(poll=self, vote__gte=0).aggregate(Sum('vote')).get('vote__sum')
        if pvotes is None:
            pvotes = 0

        nvotes = PollVoting.objects.filter(poll=self, vote__lte=0).aggregate(Sum('vote')).get('vote__sum')
        if nvotes is None:
            nvotes = 0

        self.posi = pvotes
        self.nega = nvotes
        self.score = votes
        self.save()
        # sum_lst = ptype_lst.aggregate(Sum('score'))
        # self.score = votes
        # self.save()




#planning how to attribute votes

#goals

# to make sure that contributors get awarded rightfully and get paid

# to get the bad posts excluded - solution to exclude if more then 10 votes for now

# to make sure that this works for the longer term

# so that people dont downvote thoughtlessly - solution, dont specify it for now


#plans

# 1.for the posts display only postive votes so change it to upvotes

# 2.for the posts remove posts that exceed certain negative votes - if so how many negative votes - currently leave it as 10

# 3.for the user score, I should consolidate negative votes? but for sure include negative votes - at the moment include negative votes but wait for the future to see how it goes.



        

    # def per_nega(self):
    #     total = self.posi + self.nega
    #     try:
    #         nega = float(self.nega) / total
    #         nega = str(round(nega, 2))
    #     except:
    #         nega = 0
    #     return nega

    # def per_posi(self):
    #     total = self.posi + self.nega
    #     try:
    #         posi = float(self.posi) / total
    #         posi = str(round(posi, 2))
    #     except:
    #         posi = 0
    #     return posi

    #counts the number of votes for poll - is this truly required?
    # def sum_vote_count(self):
    #     ptype = PollItem.objects.get(id=self.id)
    #     ptype_lst = PollItem.objects.filter(polltype_id=ptype.polltype.id)
    #     sum_lst = ptype_lst.aggregate(Sum('score'))
    #     ptype = Ptype.objects.get(id=ptype.polltype.id)
    #     ptype.vote_count = sum_lst.values()[0]
    #     ptype.save()

        return self.title


    class Meta:
        verbose_name = 'poll'
        verbose_name_plural = 'polls'

    def __str__(self):
        return self.title






Score = (
    (-1, "-1"),
    (0, "0"),    
    (1, "1")
)


# class PollVote(models.Model):
#     # polltype = models.ForeignKey(Ptype, blank=True, null=True, default=None)
#     vote_user = models.ForeignKey(User, on_delete=models.PROTECT)

#     # score = models.IntegerField(choices=Score, default="0")
#     posi = models.BooleanField(default=False)
#     nega = models.BooleanField(default=False)

#     poll = models.ForeignKey(PollItem, on_delete=models.PROTECT, blank=True, default=None)

#     # insert month and year?
#     date = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return "%s" %(self.vote_user)






class PollVoting(models.Model):
    vote_user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(PollItem, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" %(self.vote_user)



# include polltype because you will need favourites to be removed if it is required?

# class PollFav(models.Model):
#     # polltype = models.ForeignKey(Ptype, blank=True, default=None)
#     fav_user = models.ForeignKey(User)
#     poll = models.ManyToManyField(PollItem, blank=True, default=None)
#     # poll = models.ForeignKey(PollItem, blank=True, default=None)
#     updated = models.DateTimeField(auto_now=True)

#     def __unicode__(self):
#         return "%s" %(self.fav_user)



# include polltype because you will need favourites to be removed if it is required?

class PollFav(models.Model):
    # polltype = models.ForeignKey(Ptype, blank=True, default=None)
    # fav_user = models.ForeignKey(User, on_delete=models.PROTECT)
    # models.OneToOneField(settings.AUTH_USER_MODEL)
    fav_user = models.OneToOneField(User, on_delete=models.CASCADE)
    poll = models.ManyToManyField(PollItem, blank=True, default=None)
    # poll = models.ForeignKey(PollItem, blank=True, default=None)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" %(self.fav_user)




# @receiver(post_save, sender=PollVote, dispatch_uid='PollVote_save_signal')
# @receiver(post_delete, sender=PollVote, dispatch_uid='PollVote_delete_signal')
# def calc_score(sender, instance, using, **kwargs):
#     poll = instance.poll
#     poll.calc_score()







class SuggestedPoll(models.Model):

    typechoices = (
        ('SG', 'Suggestions'),
        ('RS', 'Recommendations')
    )

    typePoll = models.CharField(max_length=20, choices=typechoices, blank=True, default=None)
    title = models.CharField(max_length=250, unique=True)
    user_submit = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_user = models.ManyToManyField(User, blank=True, default=None, related_name='vote_user')
    allowed = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return "%s" %(self.title)

    def sugg_score(self):
        votes = SuggestedPoll.objects.get(id=self.id).vote_user.count()
        self.score = votes
        self.save()








