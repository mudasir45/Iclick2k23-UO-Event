from django.conf import settings
from django.core.mail import send_mail

def resert_send_mail_request(email, token):
    subject = 'Reset password link click here to reset your password'
    message = f'http://127.0.0.1:8000/accounts/confirmReset/{token}/'
    message_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, message_from, recipient_list)
    return True