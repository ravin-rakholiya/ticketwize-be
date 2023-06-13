from rest_framework.serializers import (ModelSerializer,)
from rest_framework import serializers
from user.models import *

class AddressSerializer(serializers.ModelSerializer):

	class Meta:
		model = Address
		fields = ['id', 'house_no', 'street', 'city', 'provision', 'country', 'postal_code']
	