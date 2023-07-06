from user.models import *
from payment.models import *
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout_payment(user_event):
	payment_method_type = "card",
	mode = "payment"
	currency = "cad"
	product_data={"name":f"{user_event.user.first_name} {user_event.user.last_name}", "email" : user_event.user.email}
	no_of_tickets = user_event.no_of_tickets
	event_fees = user_event.event.price
	service_fees = user_event.event.payment_config.service_fee
	payment_charge = user_event.event.payment_config.payment_fee
	total_fees = ((no_of_tickets*(event_fees) + (no_of_tickets*((event_fees*(service_fees+payment_charge))/100))))*100
	success_url = settings.SITE_URL+"/components/blocks/Payment/PaymentSuccess/?success=true&session_id={CHECKOUT_SESSION_ID}"
	cancle_url = settings.SITE_URL+"/components/blocks/Payment/PaymentCancle/?canceled=true"
	transaction_details = {"user_event_id":user_event.id,"payment_method_type":payment_method_type, "no_of_tickets":no_of_tickets, "mode": mode, "currency":currency, "product_data":product_data, "unit_amount":total_fees}
	payment = Payment.objects.create(user_event = user_event, transaction_details = transaction_details)
	try:
		checkout_session = stripe.checkout.Session.create(
			customer_email=user_event.user.email,
			line_items=[
				{
				# 'price': user_event.event.payment_product_id,
				'quantity': 1,
				'price_data':{
					'currency': 'cad',
					'unit_amount': int(total_fees),
					'product_data':{
					'name': f"{no_of_tickets}"+" Tickets for " + user_event.event.title
					}
				}
				},
			],
			payment_method_types = ['card'],
			mode='payment',
			success_url=success_url,
			cancel_url=cancle_url,
		)
		event = user_event.event
		event.booked_seat += int(no_of_tickets)
		event.save()
		payment.status = True
		payment.save()
		return checkout_session
	except Exception as e:
		return str(e)