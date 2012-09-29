# -*- coding: iso-8859-15 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

DOCUMENT_TYPES = ( ('ci', 'Carta d\'identita\''), ('pp', 'Passaporto'), ('pa', 'Patente')   )

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    doc_type = models.CharField(max_length=2, choices=DOCUMENT_TYPES, blank=True)
    doc_id = models.CharField(max_length=20, blank=True)
    born_date = models.DateField(blank=True, null=True)
    born_place = models.CharField(max_length=50, blank=True)

    photo = models.ImageField(upload_to='photo/', blank=True) #TODO fare check nel form per size ed eventualmente resizing
    
    date_inserted = models.DateField(auto_now_add=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
