from rest_framework.serializers import (ModelSerializer,)
from rest_framework import serializers
from user.models import *
from payment.models import Payment
from payment.serializers import PaymentSerializer

class AddressSerializer(serializers.ModelSerializer):

	class Meta:
		model = Address
		fields = ['id', 'house_no', 'street', 'city', 'provision', 'country', 'postal_code']

class UserEventSerializer(serializers.ModelSerializer):
	payment = serializers.SerializerMethodField()
	
	class Meta:
		model = UserEvent
		fields = ['id', 'user_event_id', 'payment']
	
	def get_payment(self, obj):
		payments = Payment.objects.filter(user_event = obj)
		return PaymentSerializer(payments, many=True).data