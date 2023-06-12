from django.contrib import admin
from event.models import *
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    """ Registering the Event to Django Admin Panel """
    fields = ['title', 'start_date_time', 'end_date_time', 'description', 'price', 'total_seat', 'booked_seat', 'event_type', 'sponser_by', 'artwork_by', 'organized_by', 'is_active', 'payment_config']
    list_display = ('id', 'title', 'start_date_time', 'end_date_time', 'description', 'price', 'event_id', 'total_seat', 'booked_seat', 'event_type', 'sponser_by', 'artwork_by', 'organized_by', 'is_active', 'payment_config', 'created_at', 'updated_at')
    list_per_page = 25

admin.site.register(Event, EventAdmin)