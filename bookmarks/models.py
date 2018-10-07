from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from tagging.registry import register
from bookmarks import settings

class Bookmark(models.Model):
    created = models.DateTimeField( default = timezone.now )
    title = models.CharField(max_length=settings.MAX_BOOKMARK_TITLE_LENGTH,
			blank=True, default='')
    description = models.TextField(max_length=settings.MAX_BOOKMARK_DESCRIPTION_LENGTH, 
			 blank=True, default='')
    url = models.TextField(max_length=settings.MAX_BOOKMARK_URL_LENGTH, default='')
    owner = models.ForeignKey('auth.User',related_name='bookmark', on_delete=models.CASCADE)
    public = models.BooleanField( blank=True, default = False )

    objects = models.Manager()

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.title)

# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Register with tagging app
register( Bookmark )
