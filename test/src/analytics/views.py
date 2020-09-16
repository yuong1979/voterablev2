from django.shortcuts import render

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
# Create your views here.
from tags.models import TagPoll, runtagcount
from polls.models import Ptype, PollItem
from analytics.models import PostReport
from django.contrib.auth.models import User
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from celery.schedules import crontab
from celery.task import periodic_task
from celery import shared_task, task, app

import json
import re
import urllib.request
# from pytube import YouTube
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.db.models import Count, Sum


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





def AnalyseTags(request):
	taglist = TagPoll.objects.filter(active=True)
	polllist = Ptype.objects.filter(active=True).order_by('-date')

	context = {
				'polls': polllist, 
				'tags': taglist, 
				}
				
	return render(request, 'analysetags.html', context)


def AnalysePvote(request):
	# only filtered for the top 50 lowest score so that it will not take a long time to load
	tiplist = PollItem.objects.filter(allowed=True).order_by('score')[:50]
	context = {'tiplists': tiplist,}
				
	return render(request, 'analysepvote.html', context)



def AnalyseVid(request):
	pitems = PollItem.objects.filter(published=False)
	context = {'pitems': pitems,}

	return render(request, 'analysevid.html', context)





def AnalyseComplaint(request):
	pitems = PollItem.objects.filter(published=False)
	Allreports = PostReport.objects.filter()
	report = PollItem.objects.annotate(dcount=Count('postreport__p_item')).order_by('-dcount')[:20]

	context = {
		'report': report,
		}

	return render(request, 'Analysecomplaint.html', context)













def RunOps(request):

	if request.user.is_staff == True:

		ErrorReport.delay()	

	return redirect("Home")




@task()
def ErrorReport():

	subject = "Ops Processes"

	if settings.TYPE == "base":
		from_email = settings.EMAIL_HOST_USER
	else:
		from_email = settings.DEFAULT_FROM_EMAIL

	to_email = [from_email]

	try:

		async_vid_analytics()
		loadcredit()

		contact_message = "Processes are successful"

	except Exception as e:

		print(e)

		contact_message = "Processes are not successful : " + str(e)

		
	async_contact_mail.delay(
		subject=subject,
		contact_message=contact_message,
		from_email=from_email,
		to_email=to_email
		)







# Loading the youtube credit into the source
def loadcredit():
	tiplist = PollItem.objects.filter(allowed=True)
	api_key = settings.YOUTUBE_SECRET
	p_id = []

	for i in tiplist:

		testvid = i.description

		try:
			start = testvid.index("youtube.com/embed")
			end = (testvid[start:].index('"'))
			end = start + end
			youtubefull = testvid[start:end]

			try:
				vidid = re.search(r'youtube.com/embed/(.*?)start', youtubefull).group(1)
				#remove the last question mark
				vidid = vidid[:-1]

			except AttributeError:

				vidid = re.findall('(?<=embed/).*$', youtubefull)
				#remove the item from the list
				vidid = vidid[0]

			video_id = vidid

			url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"

			json_url = urllib.request.urlopen(url)
			data = json.loads(json_url.read())


			if data.get('pageInfo')['totalResults'] != 0:
				vidcredit = data.get('items')[0]['snippet']['channelTitle']
				# print (data.get('items')[0]['snippet']['thumbnails']['default']['url'])
				# print (data.get('items')[0]['snippet']['channelTitle'])
				# print (data.get('items')[0]['snippet']['title'])



				if i.textatt == None:
					# replacing the source credit with the youtube video creator
					i.textatt = vidcredit
					i.save()

		except ValueError:
			pass
			# print ("video does not exist - skip")
	
	print ("loadcredit success")
	return None



##### local database
# 	# 15 - video is private
# 	# 34 - video is unavailable
# 	# 36 - video does not exist
# 	# 18 - works from the middle
# 	# 21 - works from the start




# for detecting dead videos
def async_vid_analytics():

	#change all the published to postive first
	posiall = PollItem.objects.filter()

	for i in posiall:
		i.published = True
		i.save()


	tiplist = PollItem.objects.filter(allowed=True)

	api_key = settings.YOUTUBE_SECRET
	p_id = []

	for i in tiplist:

		testvid = i.description

		try:
			start = testvid.index("youtube.com/embed")
			end = (testvid[start:].index('"'))
			end = start + end
			youtubefull = testvid[start:end]

			try:
				vidid = re.search(r'youtube.com/embed/(.*?)start', youtubefull).group(1)
				#remove the last question mark
				vidid = vidid[:-1]

			except AttributeError:

				vidid = re.findall('(?<=embed/).*$', youtubefull)
				#remove the item from the list
				vidid = vidid[0]

			video_id = vidid

			url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"

			json_url = urllib.request.urlopen(url)
			data = json.loads(json_url.read())

			vidactive = data.get('pageInfo')['totalResults']

			if vidactive == 0:
				print (video_id + " video is no longer existing - record result")
				p_id.append(i.id)
				print ("non working vids flagged")

		except ValueError:
			pass
			# print ("video does not exist - no issues skip")


		notvalidvid = PollItem.objects.filter(allowed=True, id__in=p_id)


	#change all the published to postive first
	FailVid = PollItem.objects.filter(id__in=p_id)

	for i in FailVid:

		i.published = False
		i.save()





# for recording users who view a specific poll - when everytime when users click n view more - disabled currently
def api_ops(request):

    if request.GET:

        if request.user.is_authenticated:
            tag_id =  request.GET.get('data')
            result = tag_id

            return JsonResponse({"result": result})
        else:
            return JsonResponse({"result": "error", "msg": "login_requred"})

    else:
        return redirect('/')






# @csrf_exempt # ok to exempt no input
# def api_ops(request):

#   if request.POST:

#       if request.user.is_authenticated:
#           tag_id =  request.POST.get('tag_id')
#           tagitem_obj = TagPoll.objects.get(id=tag_id)
#           tag_fav = TagPoll.objects.filter(title=tagitem_obj, tagfav=request.user)

#           if tag_fav:
#               # remove favorite
#               tag_fav.first().tagfav.remove(request.user)
#               result = "unfavorited"
#               # messages.info(request, "Unfavorited!")

#           else:
#               # add favorite
#               fav = TagPoll.objects.get_or_create(title=tagitem_obj)[0]
#               fav.save()
#               fav.tagfav.add(request.user)
#               result = "favorited"
#               # messages.info(request, "Favorited!")

#           return JsonResponse({"result": result})
#       else:
#           return JsonResponse({"result": "error", "msg": "login_requred"})

#   else:
#       return redirect('/')















#analyze vid backup





# def AnalyseVid(request):
# 	polllist = Ptype.objects.filter(active=True)
# 	tiplist = PollItem.objects.filter(allowed=True)

# 	api_key = settings.YOUTUBE_SECRET



# 	poll = PollItem.objects.filter(allowed=True, id=18).first()

# 	testvid = poll.description

# 	try:
# 		start = testvid.index("youtube.com/embed")
# 		end = (testvid[start:].index('"'))
# 		end = start + end
# 		youtubefull = testvid[start:end]

# 		try:
# 			vidid = re.search(r'youtube.com/embed/(.*?)start', youtubefull).group(1)
# 			#remove the last question mark
# 			vidid = vidid[:-1]

# 		except AttributeError:

# 			vidid = re.findall('(?<=embed/).*$', youtubefull)
# 			#remove the item from the list
# 			vidid = vidid[0]

# 		video_id = vidid

# 		url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"

# 		json_url = urllib.request.urlopen(url)
# 		data = json.loads(json_url.read())

# 		try:
# 			print (data.get('pageInfo')['totalResults'])

# 		except IndexError:
# 			print ("video is no longer existing")
# 			print (data.get('items')[0]['snippet']['thumbnails']['default']['url'])
# 			print (data.get('items')[0]['snippet']['channelTitle'])
# 			print (data.get('items')[0]['snippet']['title'])

# 	except ValueError:
# 		print ("video does not exist")



# 	vid = []	
# 	p_id = []

# 	# for detecting dead videos
# 	for i in tiplist:
# 		tipviddes = i.description
# 		y = tipviddes.find("youtube.com/embed")

# 		#if youtube is detected then search for the videos
# 		if y != -1:
# 			vidfound = tipviddes[y:]
# 			x = vidfound.find('"')

# 			x = y + x
# 			# print (tipviddes[y:x])

# 			# if the vid is no longer working - then append
# 			p_id.append(i.id)

# 			# ptype.append(i.polltype)
# 			# tip.append(i)
# 			vid.append(tipviddes[y:x])




# 	pitem = PollItem.objects.filter(id__in=p_id)

# 	context = {
# 				'pitems': pitem,
# 				'data': data,
# 				'vid' : vid,
# 				}
				
# 	return render(request, 'analysevid.html', context)

