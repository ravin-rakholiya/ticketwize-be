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
		event_id = request.data.get('event_id', None)
		no_of_tickets = request.data.get('no_of_tickets', None)
		first_name = request.data.get('first_name', None)
		last_name = request.data.get('last_name', None)
		email = request.data.get('email', None)
		contact_number = request.data.get('contact_number', None)
		dob = datetime.strptime(request.data.get('dob', None), '%Y-%m-%d')
		gender = request.data.get('gender', None)

		if event_id is not None:
			event = Event.objects.filter(event_id = event_id, is_active = True)
			if event:
				user = User.objects.filter(email = email)
				if user:
					user = user.last()
				else:
					user = User.objects.filter(contact_number = contact_number)
					if user:
						user = user.last()
				if user is None:
					user = User.objects.create(first_name = first_name, last_name = last_name, email = email, contact_number = contact_number, dob = dob, gender = gender)
			else:
				return Response({"response":"event is not present."},  status=status.HTTP_400_BAD_REQUEST)
			if user and event:
				event = event.last()
				if int(event.total_seat) - int(event.booked_seat) >= int(no_of_tickets):
					user_event = UserEvent.objects.create(user = user, event = event, no_of_tickets = int(no_of_tickets))
					# write a code for payment gateway after creating user event and before adding booked seat
					checkout_session = checkout_payment(user_event)
					return redirect(checkout_session.url, code=303)
					# return Response({"response": "tickets confirmation is in progress."}, status = status.HTTP_200_OK)
				else:
					return Response({"response":"reuqired seats are not available."},  status=status.HTTP_400_BAD_REQUEST)
		return Response({"response":"provide valid event id."},  status=status.HTTP_400_BAD_REQUEST)








