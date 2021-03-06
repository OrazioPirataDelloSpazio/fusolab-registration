# -*- coding: iso-8859-15 -*-
from django.db.models.signals import post_save
from django.template import Context, Template
from django.template.loader import get_template
from django.dispatch import receiver
from django.core.mail import EmailMessage
from bar.models import *
from django.conf import settings

#"value 1 is %s, value 2 is %s." % (value1, value2)

DATE_FORMAT = "%d-%m-%Y"
TIME_FORMAT = "%H:%M:%S"

@receiver(post_save, sender=BarBalance)
def bar_handler(sender, **kwargs):
    saved_balance = kwargs['instance']

    if saved_balance.operation == CLOSING:
        d = get_bar_summary(saved_balance)
        if ('warning' in d):
            template = get_template('base/bar_mail.html')
            context = Context(d)
            content = template.render(context)
            subject = 'WARNING riepilogo bar '+saved_balance.parent.date.strftime("%d/%m/%Y")
            msg = EmailMessage(subject, content, 'cassafusolab@gmail.com', to=settings.EMAIL_NOTIFICATION_LIST)
            msg.content_subtype = "html"
            msg.send()

@receiver(post_save, sender=SmallBalance)
def small_handler(sender, **kwargs):
    saved_balance = kwargs['instance']

    if saved_balance.operation == CASHPOINT:
        d = get_small_summary(saved_balance)
        if ('warning' in d):
            template = get_template('base/smallbalance_mail.html')
            context = Context(d)
            content = template.render(context)
            subject = 'WARNING riepilogo interregno '+saved_balance.date.strftime("%d/%m/%Y")
            msg = EmailMessage(subject, content, 'cassafusolab@gmail.com', to=settings.EMAIL_NOTIFICATION_LIST)
            msg.content_subtype = "html"
            msg.send()


