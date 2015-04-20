#~*~ coding: utf-8 ~*~
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.ForeignKey(User, null=True)
    birthday = models.DateField(blank=True, null=True)
    language = models.CharField( max_length=10, choices=settings.LANGUAGES, default='ru')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))


def user_post_save(sender, instance, **kwargs):
    (profile, new) = UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(user_post_save, sender=User)
