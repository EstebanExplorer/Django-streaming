from django.urls import re_path

from streaming.consumers import ConnectSignal


#https://stackoverflow.com/questions/54107099/django-channels-no-route-found-for-path
websocket_urlpatterns = [
    re_path(r'ws/', ConnectSignal.as_asgi()),
    #re_path(r'ws/negocio/(?P<room_name>[^/]+)/$', ConnectSignal.as_asgi()),
  
]

