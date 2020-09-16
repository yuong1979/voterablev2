# import requests
# import json

# CONSOLE_TOKEN = 'd2VWV6gw-vQ:APA91bHttyDftweBdUcE9Ih72fsdyqNvTKsxnULxUH8zUGNxUWXLzFRokqkJZ5DYbvqfeFDZDfmlwjFQQzs9WNwupUo3EBWCrcYqTP94fnXHJMD_HO8_T4rsjUxTl0vKVtEzyoO9BTRm'
# SERVER_KEY = 'AAAAwzumhNY:APA91bGN8Gwj7-vwre05XzZcrQFXBDxd-NIOQjlpE_kcfPOSP_o0k2ECxzgQH0fh_LJhWDlz9H4ROTlho40H4Qf39xX3FQ42FOjQM0PrINq_30ewgIHTDkdeKhh3OCdMMIi_5HsQC4UH'
# MESSAGE_TITLE = 'FireBase Message'
# MESSAGE_TEXT = 'Firebase is awesome'

# headers = {
#     'Authorization':'key={}'.format(SERVER_KEY),
#     'Content-Type': 'application/json'
# }

# data = {
#    "notification": {
#         "title": MESSAGE_TITLE,
#         "body": MESSAGE_TEXT,
#         "click_action": "http://localhost:8000/",
#         "icon": "http://localhost:8000/static/img/voterablelogo.png"
#     },
#     "to": CONSOLE_TOKEN
# }

# r = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(data) , headers=headers)
# print(r.text)