from rest_framework.serializers import (ModelSerializer,)
from rest_framework import serializers
from content.models import *

class EventContentSerializer(serializers.ModelSerializer):
	content = serializers.SerializerMethodField()

	class Meta:
		model = EventContent
		fields = ['id', 'type_of_content', 'content', 'extention', 'duration']

	def get_content(self, obj):
		try:
			return obj.content.url
		except Exception as e:
			print(e)
			return ""