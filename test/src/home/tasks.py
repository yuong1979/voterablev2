# from celery import shared_task
# from django.conf import settings
# from django.core.mail import send_mail

# # Or if you don't want to write here code then call the function here but this is best way to write corn job code here
# # Not in views.py
# # from .views import testasyncemail




# @shared_task(name='send-email-task')
# def send_email_task():

#     print ("boom it works")

#     testasyncemail()

#     # try:
#     #     if settings.TYPE == "base":
#     #         from_email = settings.EMAIL_HOST_USER
#     #     else:
#     #         from_email = settings.DEFAULT_FROM_EMAIL

#     #     subject = "test"
#     #     contact_message = "boom it works"
#     #     form_email = "jumper23sierra@yahoo.com"  # "jumper23sierra@yahoo.com"
#     #     to_email = [from_email, form_email]  # [from_email, form_email]  # [from_email, 'jumper23sierra@yahoo.com']

#     #     send_mail(
#     #         subject=subject,
#     #         message="This is a test message from Vubon",
#     #         html_message=contact_message,
#     #         from_email=from_email,
#     #         recipient_list=to_email,
#     #         fail_silently=False
#     #     )

#     #     print("email sent!")

#     # except Exception as e:
#     #     print("email failed!", e)
#     #     pass




# #for emails to be sent asynchronously
# def testasyncemail():

#     try:
#         if settings.TYPE == "base":
#             from_email = settings.EMAIL_HOST_USER
#         else:
#             from_email = settings.DEFAULT_FROM_EMAIL

#         subject = "test"
#         contact_message = "test message"
#         form_email = "jumper23sierra@yahoo.com"
#         to_email = [from_email, form_email]  # [from_email, 'jumper23sierra@yahoo.com']

#         send_mail(
#             subject=subject,
#             message="",
#             html_message=contact_message,
#             from_email=from_email,
#             recipient_list=to_email,
#             fail_silently=False
#         )

#         print ("email sent!")

#     except:

#         print ("email failed!")

#         pass