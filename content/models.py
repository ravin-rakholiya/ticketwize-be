from django.db import models
from event.models import Event
from user.models import User
from payment.models import Payment

# Create your models here.
def content_upload_path(instance, filename):
    return 'content/{0}/{1}/{2}'.format(
        instance.event.title,
        instance.type_of_content,
        filename
        )

def event_ticket_content_upload_path(instance, filename):
	return 'eventTicket/{0}/{1}/{2}/{3}'.format(
        instance.payment.user_event.event.title,
        user.id,
        instance.id,
        filename
        )

class EventContent(models.Model):
	""" Content model for storing all types of contents """

	TYPE_OF_CONTENT = (
		("image", "Image"),
		("video", "Video"),
		("thumbnail", "Thumbnail"),
	)
	event = models.ForeignKey(Event, on_delete = models.CASCADE, null = False, blank = False)
	uploader = models.ForeignKey("user.User", on_delete=models.CASCADE,limit_choices_to={"is_active": True})
	type_of_content = models.CharField(max_length=10,choices=TYPE_OF_CONTENT,)
	content = models.FileField(upload_to=content_upload_path)
	extention = models.CharField(max_length=50, blank=True, null=True)
	duration = models.CharField(max_length=10, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
	updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)

	def __str__(self):
		return f"{self.event.title}"

	class Meta:
		ordering = ["-id"]

class EventTicketContent(models.Model):
	payment = models.ForeignKey(Payment, on_delete = models.CASCADE, null = False, blank = False)
	qr = models.FileField(upload_to=event_ticket_content_upload_path)
	user = models.ForeignKey(User,on_delete = models.CASCADE, null = False, blank = False)
	created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
	updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)

	def __str__(self):
		return f"{self.payment.user_event.event.title}"

	class Meta:
		ordering = ["-id"]