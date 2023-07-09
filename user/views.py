from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.serializers import *
from user.models import *
from datetime import datetime


# Create your views here.
class FetchEventsTicketsAPIView(APIView):
	permission_classes = []
	serializer_classes = []

	def get(self, request):
		try:
			event_id = request.query_params['event_id']
			user_event_id = request.query_params['user_event_id']
			email = request.query_params['email']
			user_events = UserEvent.objects.filter(user_event_id = user_event_id)
			user_event_data = UserEventSerializer(user_events, many=True).data
			return Response({"response": user_event_data}, status = status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response({"response":"unprocessable entity."},  status=status.HTTP_400_BAD_REQUEST)