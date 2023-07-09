from django.contrib import admin
from payment.models import *

# Register your models here.
class PaymentConfigAdmin(admin.ModelAdmin):
    """ Registering the Event to Django Admin Panel """
    fields = ['service_fee', 'payment_fee', 'flat_fee']
    list_display = ('id','service_fee', 'payment_fee', 'flat_fee','created_at', 'updated_at')
    list_per_page = 25

admin.site.register(PaymentConfig, PaymentConfigAdmin)

# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    """ Registering the Event to Django Admin Panel """
    fields = ['user_event', 'transaction_details', 'status']
    list_display = ('id','user_event', 'transaction_details', 'status', 'payment_id','created_at', 'updated_at')
    list_per_page = 25

admin.site.register(Payment, PaymentAdmin)