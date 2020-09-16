from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.views.generic.base import View
from messaging.models import Message
from django.contrib import messages
from notifications.models import Notification
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
# from django.conf import settings
import json


def allin(request):
	# show all the notifications in the allin page
	notifications = Notification.objects.all_for_user(request.user).order_by('-timestamp')
	context = {
		"notifications":notifications[:30],
	}
	return render(request, "notifications/allin.html", context)

@login_required
def readall(request):

	#mark everything as read
	try:
		n_all = Notification.objects.filter(read=False, active=True, recipient=request.user)
		for i in n_all:
			i.read=True
			i.save()

		messages.info(request, "All Messages Read")

	except:
		raise HttpResponseRedirect(reverse("notifications_all"))
	return redirect('notifications_all')



@login_required
def read(request, id):
	#everytime a notification is clicked on it will mark as read
	try:
		next = request.GET.get('next', None)
		notification = Notification.objects.get(id=id)
		if notification.recipient == request.user:

			notification.read = True
			notification.save()
			if next is not None:
				return HttpResponseRedirect(next)
			else:
				return HttpResponseRedirect(reverse("notifications_all"))
		else:
			raise Http404
	except:
		raise HttpResponseRedirect(reverse("notifications_all"))


@login_required
def get_notifications_ajax(request):
	if request.is_ajax() and request.method == 'POST':

		notifications = Notification.objects.all_for_user(request.user).recent()
		count = notifications.count()
		notes = []
		for note in notifications:
			notes.append(str(note))
		data = {
			"notifications":notes,
			"count": count,
		}
		json_data = json.dumps(data)
		#returning a httpresponse, it could be return httpresponse("<h1>dude!</h1>")
		return HttpResponse(json_data, content_type="application/json")
	else:
		raise Http404


class MsgCountView(View):
	def get(self, request, *args, **kwargs):
		#counting the number of notification a users have on the navbar
		if request.user.is_authenticated:
			
			notifications = Notification.objects.all_for_user(request.user).unread()
			# removed recent because you want to show how many unread messages instead of only recent ones
			# notifications = Notification.objects.all_for_user(request.user).recent()

			count = notifications.count()
			request.session["unread_count"] = count
			return JsonResponse({"count": count })
		else:
			raise Http404

