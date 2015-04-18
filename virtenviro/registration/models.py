#~*~ coding: utf-8 ~*~
from django.db import models
from django.contrib.auth.models import User


class UserProfile( models.Model ):
    user = models.ForeignKey( User, null = True )
    birthday = models.DateField( blank = True, null = True )
    language = models.CharField( max_length = 2, choices = LANGUAGES, default = 'ru' )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )


def user_post_save(sender, instance, **kwargs):
    ( profile, new ) = UserProfile.objects.get_or_create(user=instance)


models.signals.post_save.connect(user_post_save, sender=User)
