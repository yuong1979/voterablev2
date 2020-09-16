from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

from celery.schedules import crontab
from celery.task import periodic_task
from celery import shared_task, task, app


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

# this us using a form to so that data is send to the back end to check for xxs/sql injection
from django import forms



@task()
def async_survey_mail(subject, contact_message, from_email, to_email):
    send_mail(
        subject=subject,
        message="",
        html_message=contact_message,
        from_email=from_email,
        recipient_list=to_email,
        fail_silently=False
    )


class surveyForm(forms.Form):
    # user_id = forms.CharField()
    review_id = forms.CharField()
    star_id = forms.IntegerField()

def api_survey(request):

	if request.POST:

		if request.user.is_authenticated:
			#inserts the posted ajax into the form to check for issues
			form = surveyForm(request.POST)

			if form.is_valid():
				review = form.cleaned_data['review_id']
				stars = form.cleaned_data['star_id']

				subject = "Voterable Survey"

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


				contact_message = "User " + str(request.user) + " --- " + str(stars) + " stars: " + str(review)

				# old send email with does not send asynchronously
				# send_mail(
				# 	subject=subject,
				# 	message= str(stars) + " stars : " + str(review),
				# 	html_message=contact_message,
				# 	from_email=from_email,
				# 	recipient_list=to_email,
				# 	fail_silently=False
				# )

				async_survey_mail.delay(
					subject=subject,
					contact_message=contact_message,
					from_email=from_email,
					to_email=to_email
					)

				result = "Success"

				return JsonResponse({"result": result })
			else:
				result = "Error"

				return JsonResponse({"result": result })				



		else:
			return redirect('/')



