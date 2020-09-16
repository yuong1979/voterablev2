# from fcm.utils import get_device_model
# import requests
# import json
# import logging


# class FirebaseMessenger:

#     def __init__(self,message,title):
#         self.message = message
#         self.title = title
#         self.send_messages()


#     def post_to_firebase(self, token):
#         CONSOLE_TOKEN = token
#         SERVER_KEY = 'AAAAwzumhNY:APA91bGN8Gwj7-vwre05XzZcrQFXBDxd-NIOQjlpE_kcfPOSP_o0k2ECxzgQH0fh_LJhWDlz9H4ROTlho40H4Qf39xX3FQ42FOjQM0PrINq_30ewgIHTDkdeKhh3OCdMMIi_5HsQC4UH'
#         MESSAGE_TITLE = self.title
#         MESSAGE_TEXT = self.message

#         headers = {
#             'Authorization': 'key={}'.format(SERVER_KEY),
#             'Content-Type': 'application/json'
#         }

#         data = {
#             "notification": {
#                 "title": MESSAGE_TITLE,
#                 "body": MESSAGE_TEXT,
#                 "click_action": "http://localhost:8000/",
#                 "icon": "http://localhost:8000/static/img/voterablelogo.png"
#             },
#             "to": CONSOLE_TOKEN
#         }

#         r = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=headers)
#         logging.debug(r.json())

#     def send_messages(self):

#         Device = get_device_model()

#         devices = Device.objects.all()
#         for device in devices:
#             logging.debug('Sending Message to : {}'.format(device.reg_id))
#             self.post_to_firebase(device.reg_id)


