

from django.urls import path
from streaming import views

app_name = 'streaming'

urlpatterns = [
    path('', views.dsv, name='dsv'),
    path('streaming/cam1', views.cam1, name='cam1'),
    path('streaming/cam2', views.cam2, name='cam2'),
    path('streaming/cam3', views.cam3, name='cam3'),
    path('streaming/cam4', views.cam4, name='cam4'),
]
