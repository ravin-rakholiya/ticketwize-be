from django.db import models
import pytz
import random
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import ValidationError
from event.models import Event
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=self.normalize_email(username),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
	CHEAT_OTP = ['000000', '123456', '111111']
	GENDER_CHOICES = (
		("M", "Male"),
		("F", "Female"),
		("O", "Other"),
	)

	USER_TYPE = (
		("admin", "Admin"),
		("organizer", "Organizer"),
		("normal", "Normal"),
	)

	def save(self, *args, **kwargs):
		if self.pk == None:
			if self.email:
				self.email = self.email.lower()
		super(User, self).save(*args, **kwargs)

	def validate_contact_number(value):
		global user_id
		if not (value == None or value == ""):
			if len(value) < 5 or len(value) > 16:
				raise ValidationError("Phone Number Must be in range of 5 to 16 digits")
		else:
			return value
	first_name = models.CharField(max_length=128, unique=False, blank=True, null=True, )
	last_name = models.CharField(max_length=128, unique=False, blank=True, null=True, )
	email = models.EmailField(blank=True, null=True, db_index=True, unique = True)
	contact_number = models.CharField(validators=[validate_contact_number],max_length=16, blank=True, null=True, db_index=True)
	dob = models.DateField(blank=True, null=True, )
	gender = models.CharField(max_length=1,choices=GENDER_CHOICES, blank=True, null=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	user_type = models.CharField(max_length=10,choices=USER_TYPE, blank=False, null=False, default="normal")
	created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
	updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
	objects = UserManager()

	USERNAME_FIELD = "email"

    # def has_perm(self, perm, obj=None):
    #     user_perms = []
    #     if self.is_staff:
    #         groups = self.groups.all()
    #         for group in groups:
    #             perms = [(f"{x.content_type.app_label}.{x.codename}") for x in group.permissions.all()]
    #             user_perms += perms

    #         if perm in user_perms:
    #             return True
    #     return (self.is_admin or self.is_superuser)

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		return True

class Address(models.Model):
	user = models.ForeignKey(User, null=False, blank=False, on_delete=models.PROTECT)
	event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.PROTECT)
	house_no = models.CharField(max_length=40, blank=True, null=True)
	street = models.CharField(max_length=40, blank=True, null=True)
	city = models.CharField(max_length=40, blank=True, null=True)
	provision = models.CharField(max_length=40, blank=True, null=True)
	country = models.CharField(max_length=40, blank=True, null=True)
	postal_code = models.CharField(max_length=40, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
	updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
	is_event_address = models.BooleanField(default = False)

	def __str__(self):
		return f"{self.id}--{self.user.first_name}--{self.user.last_name}"

	class Meta:
		ordering = ["-id"]

class UserEvent(models.Model):
	user = models.ForeignKey(User, null=False, blank=False, on_delete=models.PROTECT)
	event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.PROTECT)
	no_of_tickets = models.IntegerField(blank=False, null=False, default = 0)
	created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
	updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
	
	def __str__(self):
		return f"{self.id}"

	class Meta:
		ordering = ["-id"]