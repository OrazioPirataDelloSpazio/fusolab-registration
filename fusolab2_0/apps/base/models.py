# -*- coding: iso-8859-15 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.core.cache import cache
from decimal import Decimal 
from datetime import *
from django.conf import settings
#from sorl.thumbnail import ImageField

DOCUMENT_TYPES = ( ('ci', 'Carta d\'identita\''), ('pp', 'Passaporto'), ('pa', 'Patente')   )
DATE_FORMAT = "%d-%m-%Y" 
TIME_FORMAT = "%H:%M:%S"

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    doc_type = models.CharField(max_length=2, choices=DOCUMENT_TYPES, blank=True)
    doc_id = models.CharField(max_length=20, blank=True)
    born_date = models.DateField(blank=True, null=True)
    born_place = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='photo/', blank=True) #TODO fare check nel form per size ed eventualmente resizing
    how_hear = models.CharField(max_length=500, blank=True)
    salutatore = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)

    def get_photo(self):
        return self.photo if self.photo else '/static/images/fusolab_unnamed.jpg'

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.now()
            if now > self.last_seen() + timedelta(
                         seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

	class Meta:
		verbose_name = "Utente"
		verbose_name_plural = "Utenti"		


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


