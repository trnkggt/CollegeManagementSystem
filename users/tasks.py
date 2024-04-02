from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.conf import settings

from .tokens import email_verification_token


@shared_task
def confirmation(user_pk, domain):
    """
    Task to send a mail for user verification
    """
    user = get_user_model().objects.get(id=user_pk)
    current_site = domain
    mail_subject = "Email Verification"
    message = render_to_string('auth/activate_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': email_verification_token.make_token(user),
    })
    send_mail(mail_subject,
              message,
              settings.EMAIL_HOST_USER,
              recipient_list=[user.email, ])


@shared_task
def sent_from_admin(email_subject, email_body, to_email):
    send_mail(email_subject, email_body,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[to_email, ])