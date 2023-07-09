from django.db import models
from jsonfield import JSONField

# Create your models here.
class PaymentConfig(models.Model):
	service_fee = models.FloatField(default=0.0, null = False, blank = False)
	payment_fee = models.FloatField(default=2.99, null = False, blank = False)
	flat_fee = models.FloatField(default=1.00, null = False, blank = False)
	created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
	updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
	
	def __str__(self):
		return f"{self.id} - service fee: {self.service_fee} ** payment fee: {self.payment_fee} ** flat_fee: {self.flat_fee}"

	class Meta:
		ordering = ["-id"]


class Payment(models.Model):
	user_event = models.ForeignKey("user.UserEvent", related_name='payment_user_event',on_delete = models.PROTECT, null = False, blank = False)
	transaction_details = JSONField(null=True, blank=True)
	status =  models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
	updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)

	def __str__(self):
		return f"{self.id}"

	class Meta:
		ordering = ["-id"]
