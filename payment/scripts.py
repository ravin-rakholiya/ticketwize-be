from user.models import *
from payment.models import *
import stripe
from django.conf import settings
import qrcode
import qrcode.image.svg
from content.models import EventTicketContent

stripe.api_key = settings.STRIPE_SECRET_KEY
site_url = settings.SITE_URL

ROOT_DIR = settings.ROOT_DIR
print(f"13---{ROOT_DIR}/qr.svg")
def checkout_payment(user_event, email):
	payment_method_type = "card",
	mode = "payment"
	currency = "cad"
	product_data={"name":f"{user_event.user.first_name} {user_event.user.last_name}", "email" : user_event.user.email}
	no_of_tickets = user_event.no_of_tickets
	event_fees = user_event.event.price
	service_fees = user_event.event.payment_config.service_fee
	payment_charge = user_event.event.payment_config.payment_fee
	flat_fee = user_event.event.payment_config.flat_fee
	total_fees = ((no_of_tickets*(event_fees + flat_fee) + (no_of_tickets*((event_fees*(service_fees+payment_charge))/100))))*100
	success_url = settings.SITE_URL+"/components/blocks/Payment/PaymentSuccess/?success=true&session_id={CHECKOUT_SESSION_ID}"+"&email="+email
	cancle_url = settings.SITE_URL+"/components/blocks/Payment/PaymentCancle/?canceled=true"+"&email="+email
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

import boto3

s3_client = boto3.client('s3')

def upload_file_to_s3(qr_svg):
	s3_client.upload_file(
	    Filename=f"{ROOT_DIR}/qr.svg",
	    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
	    Key='media/content/1/image/qr.svg'
	)

# from bytesIO import bytesIO

def get_qrcode_svg(uri):
    stream = bytesIO()
    img = qrcode.make( uri, image_factory=qrcode.image.svg.SvgImage)
    img.save(stream)
    return stream.getvalue().decode()

def generate_event_ticket_qr_code(event_id, email):
	user_events = UserEvent.objects.filter(user__email = email, event__event_id = event_id)
	for user_event in user_events:
		payments = Payment.objects.filter(user_event = user_event , status = True)
		for payment in payments:
			# qr_svg = qrcode.make(f"{site_url}/ticket/?event_id={event_id}?email={email}", image_factory=qrcode.image.svg.SvgImage)
			qr_svg = get_qrcode_svg(f"{site_url}/ticket/?event_id={event_id}&email={email}&user_event_id&{user_event}")

			# with open('qr.svg', 'wb') as qr:
			# 	print(f"77----{type(qr_svg)}")
				# upload_file_to_s3(qr)






