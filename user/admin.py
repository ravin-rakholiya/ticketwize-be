from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Permission

from user.models import *
# Register your models here.
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
	def get_queryset(self, request):
		qs = super().get_queryset(request)
		return qs.select_related('content_type')


class UserCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email',)

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('email', 'password', 'contact_number', 'is_active', 'is_admin', 'is_staff')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]

class UserAdmin(BaseUserAdmin):
	# The forms to add and change user instances
	form = UserChangeForm
	add_form = UserCreationForm
	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = (
	'id', 'first_name', 'last_name', 'email', 'contact_number', 'is_admin', 'is_active', 'created_at', 'updated_at')
	list_filter = ('is_admin',)
	fieldsets = (
		(None, {'fields': ('first_name', 'last_name', 'email', 'contact_number','password')}),
		('Additional Info', {'fields': ('dob', 'gender', 'user_type')}),
		('Permissions', {'fields': ('is_staff', 'is_admin','is_active')}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {'fields': ('email', 'password1', 'password2')}),
	)
	admin.site.disable_action('delete_selected')
	search_fields = ('first_name', 'last_name','email', 'contact_number')
	ordering = ('id',)

	filter_horizontal = ()

	def has_delete_permission(self, request, obj=None):
		# Disable delete
		return False


admin.site.register(User, UserAdmin)




class AddressAdmin(admin.ModelAdmin):
    """ Registering the Address to Django Admin Panel """
    fields = ['user', 'event', 'house_no', 'street', 'city', 'provision', 'country', 'postal_code', 'is_event_address']
    list_display = ('id', 'user', 'event', 'house_no', 'street', 'city', 'provision', 'country', 'postal_code', 'is_event_address', 'created_at', 'updated_at')
    list_per_page = 25

admin.site.register(Address, AddressAdmin)


class UserEventAdmin(admin.ModelAdmin):
    """ Registering the UserEvent to Django Admin Panel """
    fields = ['user', 'event', 'no_of_tickets']
    list_display = ('id', 'user', 'event', 'no_of_tickets', 'user_event_id', 'created_at', 'updated_at',)
    list_per_page = 25

admin.site.register(UserEvent, UserEventAdmin)



