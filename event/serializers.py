from rest_framework.serializers import (ModelSerializer,)
from rest_framework import serializers
from event.models import *
from content.models import EventContent
from content.serializers import EventContentSerializer
from user.models import Address
from user.serializers import AddressSerializer

class EventSerializer(serializers.ModelSerializer):
	event_content = serializers.SerializerMethodField()
	address = serializers.SerializerMethodField()

	class Meta:
		model = Event
		fields = ['id', 'title', 'start_date_time', 'end_date_time', 'description', 'address', 'price', 'event_id', 'total_seat', 'booked_seat', 'event_type', 'sponser_by', 'artwork_by', 'organized_by', 'payment_config', 'event_content']

	def get_event_content(self, obj):
		event_content = EventContent.objects.filter(event = obj)
		return EventContentSerializer(event_content, many = True).data

	def get_address(self, obj):
		try:
			address = Address.objects.get(event = obj, is_event_address = True)
			return AddressSerializer(address).data
		except Exception as e:
			return {}
