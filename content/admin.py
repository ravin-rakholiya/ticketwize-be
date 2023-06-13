from django.contrib import admin
from content.models import *

# Register your models here.
class EventContentAdmin(admin.ModelAdmin):
    """ Registering the Event to Django Admin Panel """
    fields = ['event', 'uploader', 'type_of_content', 'content', 'extention', 'duration']
    list_display = ('id', 'event', 'uploader', 'type_of_content', 'content', 'extention', 'duration', 'created_at', 'updated_at')
    list_per_page = 25

admin.site.register(EventContent, EventContentAdmin)