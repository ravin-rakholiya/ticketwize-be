from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from payment.serializers import *
from payment.models import *
from datetime import datetime
import stripe



# Create your views here.
class FetchPaymentConfig(APIView):
	permission_classes = []
	serializer_classes = []

	def get(self, request):
		try:
			payment_config = PaymentConfig.objects.last()
			if payment_config:
				payment_config_data = PaymentConfigSerializer(payment_config).data
				return Response({"response": payment_config_data}, status = status.HTTP_200_OK)
			return Response({"response":"not found any payment_config."}, status = status.HTTP_200_OK)
		except Exception as e:
			return Response({"response":"unprocessable entity."},  status=status.HTTP_400_BAD_REQUEST)