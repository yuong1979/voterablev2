# from __future__ import absolute_import, unicode_literals
# from celery import task

# from celery.utils.log import get_task_logger
# logger = get_task_logger(__name__)
# from notifications.models import Notification
# from users.models import PUser
# from firebasenotifications.models import DeviceToken
# from firebasenotifications.views import post_to_firebase




# @task(name='send-notification-task')
# def send_custom_message():
#     usersub = PUser.objects.filter(subnewsletter=True)

#     results = []

#     for i in usersub:
#         # try to get tokens for user
#         tokens = DeviceToken.objects.filter(user_id=i.user_id, active=True)
#         if len(tokens) == 0:
#             continue

#         user = i.user

#         notinewtip = Notification.objects.filter(action='New Tip', recipient=user, read=False, active=True).count()
#         notinewtiplist = Notification.objects.filter(action='New Tip List', recipient=user, read=False,
#                                                      active=True).count()

#         if notinewtip > 0 and notinewtiplist > 0:
#             msgbody = "Hi " + str(i.user) + ", you have " + str(
#                 notinewtip) + " new tips for your favorite lists and " + str(
#                 notinewtiplist) + " new tip lists for your favorite tags."
#         elif notinewtip == 0 and notinewtiplist > 0:
#             msgbody = "Hi " + str(i.user) + ", you have " + str(
#                 notinewtiplist) + " new tip lists for your favorite tags."
#         elif notinewtiplist == 0 and notinewtip > 0:
#             msgbody = "Hi " + str(i.user) + ", you have " + str(notinewtip) + " new tips for your favorite lists."
#         elif notinewtiplist > 0 and notinewtip > 0:
#             msgbody = "Hi " + str(i.user) + ", you have " + str(
#                 notinewtip) + " new tips for your favorite lists and " + str(
#                 notinewtiplist) + " new tip lists for your favorite tags."
#         else:
#             msgbody = None

#         for token in tokens:
#             # print(msgbody, token.device_token)
#             results.append(post_to_firebase(title=f'Hi {str(i.user)}', message=msgbody, token=token.device_token))

#     return results


# @task()
# def do_something():
#     logger.info('******** CALLING ASYNC TASK WITH CELERY **********')
#     # Your code