from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from event.serializers import *
from datetime import datetime
from user.models import User, UserEvent, Address
from payment.scripts import *
from django.shortcuts import redirect
from django.conf import settings
from notifications.email_notifications import send_ticket_verification_mail
site_url = settings.SITE_URL
from_email = settings.EMAIL_HOST_USER

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
			no_of_tickets = request.data.get('no_of_tickets', None)
			first_name = request.data.get('first_name', None)
			last_name = request.data.get('last_name', None)
			email = request.data.get('email', None)
			contact_number = request.data.get('contact_number', None)
			gender = request.data.get('gender', None)
		except Exception as e:
			print(e)
		if event_id is not None:
			event = Event.objects.filter(event_id = event_id, is_active = True)
			if event:
				user = User.objects.filter(email = email)
				if user:
					user = user.last()
				else:
					user = User.objects.create(first_name = first_name, last_name = last_name, email = email, contact_number = contact_number, gender = gender)
			else:
				return Response({"response":"event is not present."},  status=status.HTTP_400_BAD_REQUEST)
			if user and event:
				event = event.last()
				if int(event.total_seat) - int(event.booked_seat) >= int(no_of_tickets):
					user_event = UserEvent.objects.create(user = user, event = event, no_of_tickets = int(no_of_tickets))
					# write a code for payment gateway after creating user event and before adding booked seat
					checkout_session = checkout_payment(user_event, email)

					return Response({"response":checkout_session.url},  status=status.HTTP_200_OK)
				else:
					return Response({"response":"reuqired seats are not available."},  status=status.HTTP_400_BAD_REQUEST)
		return Response({"response":"provide valid event id."},  status=status.HTTP_400_BAD_REQUEST)


class EventRegistrationSuccessfulAPIView(APIView):
	permission_classes = []
	serializer_classes = []

	def get(self, request):
		print(f"75---------")
		event_id = request.query_params['event_id']
		email = request.query_params['email']
		# user_event_id = request.query_params['user_event_id']
		
		try:
			event = Event.objects.get(event_id = event_id)
			if event:
				pass
			else:
				return Response({"response":"event_id is wrong."},  status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			print(e)
			return Response({"response":"exception occured with evemrr."},  status=status.HTTP_400_BAD_REQUEST)

		try:
			if email:
				user = User.objects.get(email = email)
			else:
				return Response({"response":"email not provided."},  status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			print(e)
			return Response({"response":"exception occured with user."},  status=status.HTTP_400_BAD_REQUEST)

		user_events = UserEvent.objects.filter(user = user, event = event)
		no_of_tickets = 0
		if user_events:
			for user_event in user_events:
				payments = Payment.objects.filter(user_event = user_event, status = True)
				if payments:
					no_of_tickets = no_of_tickets + user_event.no_of_tickets
		event_address = Address.objects.get(event = event)
		user_event = UserEvent.objects.filter(user = user, event = event)
		if user_event:
			user_event = user_event.last()
		email_content = {"full_name": user.first_name if user.first_name else None+" "+user.last_name if user.last_name else None, "no_of_tickets": no_of_tickets,
						"event_title": event.title, "event_date": {event.end_date_time},
						"event_venue":f"{event_address.house_no}, {event_address.street}, {event_address.city}, {event_address.provision}, {event_address.country}, {event_address.postal_code}",
						"ticket_link":f"{site_url}/components/blocks/ticket/eventTicket?event_id={event_id}&email={email}&user_event_id={user_event.user_event_id}"}
		if(user_event.success_mail == False):
			send_ticket_verification_mail(email_content, (email,), from_email)
			user_event.success_mail = True
			user_event.save()
			return Response({"response":"mail sent successfully."},  status=status.HTTP_200_OK)
		return Response({"response":"mail sent already."},  status=status.HTTP_200_OK)









