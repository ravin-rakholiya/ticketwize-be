from rest_framework.serializers import (ModelSerializer,)
from rest_framework import serializers
from payment.models import *

class PaymentConfigSerializer(serializers.ModelSerializer):
	total_additional_charges = serializers.SerializerMethodField()
	class Meta:
		model = PaymentConfig
		fields = ['service_fee', 'payment_fee', 'total_additional_charges']

	def get_total_additional_charges(self, obj):
		return obj.service_fee + obj.payment_fee