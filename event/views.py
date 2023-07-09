from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from event.serializers import *
from datetime import datetime
from user.models import User, UserEvent
from payment.scripts import *
from django.shortcuts import redirect

# Create your views here.
class FetchEventAPIView(APIView):
	permission_classes = []
	serializer_classes = []

	def get(self, request):
		try:
			event_id = request.query_params['event_id']
			event = Event.objects.filter(event_id = event_id, is_active = True)
			if event:
				event = event.last()
				event_data = EventSerializer(event).data
				return Response({"response": event_data}, status = status.HTTP_200_OK)
			return Response({"response":"not found any event."}, status = status.HTTP_200_OK)
		except Exception as e:
			return Response({"response":"unprocessable entity."},  status=status.HTTP_400_BAD_REQUEST)

class RegisterEventAPIView(APIView):
	permission_classes = []
	serializer_classes = []

	def post(self, request):
		print(request.data)
		try:
			event_id = request.data.get('event_id', None)
			print(f"35---------", event_id)
			no_of_tickets = request.data.get('no_of_tickets', None)
			print(f"36---------", no_of_tickets)
			first_name = request.data.get('first_name', None)
			print(f"37---------", first_name)
			last_name = request.data.get('last_name', None)
			print(f"38---------", last_name)
			email = request.data.get('email', None)
			print(f"39---------", email)
			contact_number = request.data.get('contact_number', None)
			print(f"40---------", contact_number)
			gender = request.data.get('gender', None)
			print(f"47-----", gender)
		except Exception as e:
			print(e)
		print(f"49--------------")
		if event_id is not None:
			print(f"51-------")
			event = Event.objects.filter(event_id = event_id, is_active = True)
			print(f"53-------")
			if event:
				print(f"54-------")
				user = User.objects.filter(email = email)
				print(f"55-------", user)
				if user:
					print(f"56-------")
					user = user.last()
					print(f"57-------")

				else:
					print(f"61-------")
					user = User.objects.create(first_name = first_name, last_name = last_name, email = email, contact_number = contact_number, gender = gender)
					print(f"53--------------")
			else:
				print(f"55----------------")
				return Response({"response":"event is not present."},  status=status.HTTP_400_BAD_REQUEST)
			if user and event:
				print(f"58---------------------")
				event = event.last()
				print(f"60---------------------")
				if int(event.total_seat) - int(event.booked_seat) >= int(no_of_tickets):
					user_event = UserEvent.objects.create(user = user, event = event, no_of_tickets = int(no_of_tickets))
					print(f"64--------------------")
					# write a code for payment gateway after creating user event and before adding booked seat
					checkout_session = checkout_payment(user_event, email)
					return Response({"response":checkout_session.url},  status=status.HTTP_200_OK)
				else:
					return Response({"response":"reuqired seats are not available."},  status=status.HTTP_400_BAD_REQUEST)
		return Response({"response":"provide valid event id."},  status=status.HTTP_400_BAD_REQUEST)








