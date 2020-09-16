from django.conf.urls import url
from firebasenotifications.views import DeviceTokenCreateView, DeviceTokenListView, send_custom_message
urlpatterns = [
    url(r'add', DeviceTokenCreateView.as_view(), name='add-fcm-device-token'),
    url(r'tokenlist/', DeviceTokenListView.as_view(), name= 'fcm-device-token-list'),
    # url(r'send/', send_topic_message, name='send-fcm-message'),
    url(r'firebase/', send_custom_message, name='send-custom-fcm-message'),
]