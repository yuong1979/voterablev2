import requests
import json

CONSOLE_TOKEN = 'fj5aFnqZing:APA91bGHOjaRAonQasQE43Usj6E_jlmwxNG0Mg7lqgzdgjM5r97iYQ-3B--Dh7b9vIw9p10TWUyvwz1bIMorysDg2xPdUJYaSWKbg6CubfUuOyFqZ1M8p0yTK4CO0KK9dpquJEC_8vT4'
SERVER_KEY = 'AAAAwzumhNY:APA91bGN8Gwj7-vwre05XzZcrQFXBDxd-NIOQjlpE_kcfPOSP_o0k2ECxzgQH0fh_LJhWDlz9H4ROTlho40H4Qf39xX3FQ42FOjQM0PrINq_30ewgIHTDkdeKhh3OCdMMIi_5HsQC4UH'
MESSAGE_TITLE = 'FireBase Message1'
MESSAGE_TEXT = 'Firebase is awesome1'

headers = {
    'Authorization':'key={}'.format(SERVER_KEY),
    'Content-Type': 'application/json'
}

data = {
   "notification": {
        "title": MESSAGE_TITLE,
        "body": MESSAGE_TEXT,
        "click_action": "http://localhost:8000/",
        "icon": "http://localhost:8000/static/img/voterablelogo.png"
    },
    "to": CONSOLE_TOKEN
}

r = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(data) , headers=headers)
print(r.text)