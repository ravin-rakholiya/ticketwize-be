from django.urls import path, include
from rest_framework import routers
from event import views


urlpatterns = [
    path('fetch', views.FetchEventAPIView.as_view(), name='fetch-event-data'),
    path('register', views.RegisterEventAPIView.as_view(), name='register-event'),
]