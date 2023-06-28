from django.db import models
import uuid
from ckeditor.fields import RichTextField
from payment.models import PaymentConfig

# Create your models here.
class Event(models.Model):
	title = models.CharField(max_length=512, blank=False, null=False)
	start_date_time = models.DateTimeField(null=False, blank=False)
	end_date_time = models.DateTimeField(null=False, blank=False)
	description = RichTextField()
	price = models.FloatField(default=0.0, null = False, blank = False)
	event_id = models.UUIDField(default = uuid.uuid4, editable = False)
	total_seat = models.IntegerField(blank=False, null=False, default = 0)
	booked_seat = models.IntegerField(blank=False, null=False, default = 0)
	event_type = models.CharField(max_length = 256, null = True, blank = True)
	sponser_by = models.CharField(max_length = 256, null = False, blank = False)
	artwork_by = models.CharField(max_length = 256, null = False, blank = False)
	organized_by = models.ForeignKey("user.User", on_delete = models.PROTECT, max_length = 128, null = False, blank = False)
	is_active = models.BooleanField(default=True)
	payment_config =  models.ForeignKey(PaymentConfig, on_delete=models.PROTECT, default = 1)
	payment_product_id = models.CharField(max_length=256, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
	updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
	
	def __str__(self):
		return f"{self.title}"

	class Meta:
		ordering = ["-id"]

