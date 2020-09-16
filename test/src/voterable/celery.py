from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
from django.conf import settings





os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voterable.settings")

# app = Celery('voterable')
app = Celery('voterable', broker=settings.CELERY_BROKER_URL)

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# ctable = ControlTable.objects.get(id=1)

# print (test.notiweekday)
# print (test.notihour)
# print (test.notiminute)




app.conf.beat_schedule = {

# comment the below to test the celery tasks


#    test send notification every 60secs - disable before going into production if not it will run this task which is unnecessary
# this should sends a notification to the users desktop

    # 'add-every-60-seconds': {
    #     'task': 'send-notification-task',
    #     'schedule': 60.0,
    # },

    # 'add-every-5-minutes': {
    #     'task': 'send-notification-task',
    #     'schedule': 300.0,
    # },


#  send notification every tuesday at 12 p.m. - change this and enable this before going live
    # 'send_noti_tuesday': {
    #     'task': 'send-notification-task',
    #     'schedule': crontab(hour=17, minute=15, day_of_week=5),
    # },



   # # test send notification every 30mins.
   #  'add-every-15-minutes': {
   #      'task': 'send-notification-task',
   #      'schedule': 900.0,
   #  },

   # # send email every 20secs.
   #  'add-every-20-seconds': {
   #      'task': 'send-test-task',
   #      'schedule': 20.0,
   #  },


# #  send notification every tuesday at 12 p.m.
#     'send_noti_tuesday': {
#         'task': 'send-notification-task',
#         'schedule': crontab(hour=12, minute=0, day_of_week=2),
#     },



### this below should be working, just minimize chrome in the background
### make sure that notification is on on your home page
### make sure that in chrome - settings - site settings - notifications has the url
#  send notification every day at 12:15 a.m.
    'send_noti_everyday': {
        'task': 'send-notification-task',
        'schedule': crontab(hour=0, minute=15),
    },





# #  test - send testing task every day at 22:29 p.m.
#     'send_test_everyday': {
#         'task': 'send-test-task',
#         'schedule': crontab(hour=22, minute=29),
#     },


}


## to run celery start redis first and open up two cmd interfaces and run the two commands below
# celery -A voterable beat -l info
# celery -A voterable worker -l info -P eventlet


# if the running of celery fails remember to delete all the celerybeat-schedule files inside voterable and try again



# to activate subscription do a search for subscriptionactivate to find all the code relevant to activating subscription




## For testing notifications
# http://localhost:8000/devicetoken/firebase/

# For testing referrals
# http://localhost:8000/?ref=T2R47J

#cron time to do backup currently at 0 16 * * * which is 1600 utc or 0000 Singapore time

# target late evening crowd in usa, early 10am crowd in india, lunchcrowd in singapore and early morning commuter crowd in europe
#for timeplaning, currently Singapore 12pm = la 8pm = london 4am = newyork 11pm = bangalore 930pm
#https://www.timeanddate.com/worldclock/converter.html?iso=20190102T040000&p1=tz_sgt&p2=137&p3=136&p4=179&p5=438



