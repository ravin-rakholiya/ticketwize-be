from django.urls import path, include
from rest_framework import routers
from payment import views


urlpatterns = [
    path('fetch/payment_config', views.FetchPaymentConfig.as_view(), name='fetch-payment-config'),
    # path('checkout', views.CheckoutPayment.as_view(), name='checkout-payment'),
]