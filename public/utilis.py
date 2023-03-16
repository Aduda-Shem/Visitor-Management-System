from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_activation_email(user):
    subject = 'Activate your account'
    html_message = render_to_string('email/user_email.html', {'first_name': user.first_name, 'activation_link': user.activation_link, 'site_name': settings.SITE_NAME})
    plain_message = strip_tags(html_message)
    from_email = 'noreply@netbot.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
