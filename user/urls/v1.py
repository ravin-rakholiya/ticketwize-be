from django.urls import path, include
from rest_framework import routers
from user import views


urlpatterns = [
    path('fetch/tickets', views.FetchEventsTicketsAPIView.as_view(), name='fetch-event-tickets'),
]