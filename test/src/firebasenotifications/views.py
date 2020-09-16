from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework import generics
from .models import DeviceToken
from .serializer import DeviceTokenSerializer
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from notifications.models import Notification
from users.models import PUser
from celery import task


#how the firebase notification should work
# when the user logs in and signs up for the first time, the prompt for notification should appear.
# if user agrees, they will be recieving notifications.
# if they want to disable the notifications they can go into the app to disable the notifications on their homepage





#how to troubleshoot for users having issues with notification
# admin can delete the device token inside firebase notifications that belongs to the user and ask user to sign in again
# if user still has issues go to chrome settings -> site settings -> notifications -> check the allowed sites
# The user also needs to enable the notifications on his/her homepage

# by right this process shouldnt need to include the user having to go into the javascript application to "clear storage"




#creating a new firebase token for users who accept notifications sending
class DeviceTokenCreateView(generics.CreateAPIView):
    queryset = DeviceToken.objects.all()
    serializer_class = DeviceTokenSerializer

    def post(self, request, *args, **kwargs):
        data = dict(request.data.dict())
        
        user = self.request.user.pk
        data['userdt'] = user

        if int(data['user_id']) != self.request.user.id:
            return JsonResponse({'message':'not allowed'},status=500)

        serializer = DeviceTokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if self.add_to_topic(data['device_token']) != 200:
            return JsonResponse({'message':'Subscription to topic failed'}, status=500)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def add_to_topic(self, token):
        headers = {
            'Authorization': 'key={}'.format(settings.SERVER_KEY),
            'Content-Type': 'application/json'
        }
        send_url = f' https://iid.googleapis.com/iid/v1/{token}/rel/topics/{settings.TOPIC_NAME}'
        r = requests.post(send_url, headers=headers)
        return r.status_code


class DeviceTokenListView(generics.ListAPIView):
    queryset = DeviceToken.objects.all()
    serializer_class = DeviceTokenSerializer


# @csrf_exempt
# def send_topic_message(request):
#     headers = {
#         'Authorization': 'key={}'.format(settings.SERVER_KEY),
#         'Content-Type': 'application/json'
#     }

#     data = {
#         "to": f"/topics/{settings.TOPIC_NAME}",
#         "priority": "high",
#         "notification": {
#             "body": settings.MESSAGE_BODY,
#             "title": settings.MESSAGE_TITLE,
#             "click_action": settings.CLICK_ACTION
#         },
#     }

#     if request.method == 'POST':
#         data = requests.POST['data']
#     r = requests.post('https://fcm.googleapis.com/fcm/send',data=json.dumps(data), headers=headers)
#     return JsonResponse({'message_sent':data,'fcm_response':r.text,'status_code':r.status_code})



#creating the message that will be sent as a notification to the user
def create_message():
    # usersub = PUser.objects.filter(subnewsletter=True)
    # extracting the notifications which are unread and identify the users
    usernoti = Notification.objects.filter(read=False, active=True).values('recipient').distinct()
    # select the users who have subscribed to the newsletter
    usersub = PUser.objects.filter(user_id__in=usernoti, subnewsletter=True)

    results = []


    # getting the tokens for each subscribed user and looping through all to send the notifications
    for i in usersub:

        print (i)


        #try retrieving tokens from each user if they are active tokens
        tokens = DeviceToken.objects.filter(user_id=i.user_id, active=True)
        if len(tokens) == 0:
            continue

        user = i.user

        notinewtip = Notification.objects.filter(action='New Tip', recipient=user, read=False, active=True).count()
        notinewtiplist = Notification.objects.filter(action='New Tip List', recipient=user, read=False,
                                                     active=True).count()

        if notinewtip > 0 and notinewtiplist > 0:
            msgbody = "Hi " + str(i.user) + ", you have " + str(
                notinewtip) + " new tips for your favorite lists and " + str(
                notinewtiplist) + " new tip lists for your favorite tags."
        elif notinewtip == 0 and notinewtiplist > 0:
            msgbody = "Hi " + str(i.user) + ", you have " + str(
                notinewtiplist) + " new tip lists for your favorite tags."
        elif notinewtiplist == 0 and notinewtip > 0:
            msgbody = "Hi " + str(i.user) + ", you have " + str(notinewtip) + " new tips for your favorite lists."
        elif notinewtiplist > 0 and notinewtip > 0:
            msgbody = "Hi " + str(i.user) + ", you have " + str(
                notinewtip) + " new tips for your favorite lists and " + str(
                notinewtiplist) + " new tip lists for your favorite tags."
        else:
            msgbody = None

        #using each token to sending notifications to each users token via firebase - because you require users token to send them notification
        for token in tokens:
            # print(msgbody, token.device_token)
            results.append(post_to_firebase(title=f'Hello {str(i.user)}', message=msgbody, token=token.device_token))

    return results





# sending a manual notification because activating it requires a request and response
def send_custom_message(request):
    results = create_message()
    return JsonResponse({'results':results})

# auto sending of notification when add-every-60-seconds is uncommented on celery.py
@task(name='send-notification-task')
def auto_send_custom_message():
    create_message()




#crafting firebase object with neccessary datas and headers so that the msgbody can be loaded into it and sent
def post_to_firebase(title, message, token, clickaction = settings.CLICK_ACTION, icon = settings.NOTIFICATION_ICON):

    headers = {
        'Authorization': 'key={}'.format(settings.SERVER_KEY),
        'Content-Type': 'application/json'
    }

    data = {
        "notification": {
            "title": title,
            "body": message,
            "click_action": clickaction,
            "icon":icon,
        },
        "to": token
    }

    r = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=headers)
    # print(r.json())
    return {'message_sent':data, 'status_code':r.status_code, 'firebase_response':r.json()}
