from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/booking/notify/(?P<resto_owner_id>\d+)/$', consumers.BookingNotificationConsumer.as_asgi()),
]
