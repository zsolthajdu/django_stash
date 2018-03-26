from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from tagging.registry import register
from tagging.fields import TagField

class Bookmark(models.Model):
    created = models.DateTimeField( default = datetime.now )
    title = models.CharField(max_length=256, blank=True, default='')
    description = models.CharField(max_length=2048, blank=True, default='')
    url = models.CharField(max_length=2048, blank=True, default='')
    owner = models.ForeignKey('auth.User',related_name='bookmark', on_delete=models.CASCADE)
    public = models.BooleanField( blank=True, default = False )

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
