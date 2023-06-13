from django.db import models
from event.models import Event
# Create your models here.
def content_upload_path(instance, filename):
    return 'content/{0}/{1}/{2}'.format(
        instance.uploader.id,
        instance.type_of_content,
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