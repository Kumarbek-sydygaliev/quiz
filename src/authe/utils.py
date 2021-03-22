from __future__ import absolute_import, unicode_literals

from django.core.mail import send_mail
from django.conf import settings

def send_verified_link(message, email):
    send_mail('Quiz', message, settings.DEFAULT_EMAIL_FROM, [email,])