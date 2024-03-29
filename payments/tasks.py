from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.html import mark_safe
from django.conf import settings

from .models import Order


@shared_task
def order_completed(first_name, email):
    """
    Task to send a mail when user successfully buys a course
    """
    subject = 'Successful order'
    message = (f'Thank you for your order {first_name}, you can check all the available classes and choose one that you like. Good luck.')
    safe_message = mark_safe(message)

    mail_sent = send_mail(subject, '',from_email=settings.EMAIL_HOST_USER,
              recipient_list=[email],html_message=safe_message)

    return mail_sent