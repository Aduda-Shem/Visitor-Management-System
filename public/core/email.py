from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail.message import sanitize_address
from django.template import loader

from email.headerregistry import Address

from public.users.models import get_user_profile_id

# Create here
def build_email(template_prefix, to_user_ids=None, to_emails=None, context=None, tenant=None):
    if to_user_ids is not None:
        to_users = [get_user_profile_id(to_user_id) for to_user_id in to_user_ids]
        if tenant is None:
            tenant = to_users[0].tenants
        to_emails = []
        for to_user in to_users:
            stringified = str(Address(display_name=to_user.full_name, addr_spec=to_user.email))
            if len(sanitize_address(stringified, "utf-8")) > 320:
                stringified = str(Address(addr_spec=to_user.email))
            to_emails.append(stringified)
    context = {
        **context, # type: ignore
        "physical_address": settings.PHYSICAL_ADDRESS,
        "support_email": settings.DEFAULT_FROM_EMAIL,
        # "email_images_base_url": settings.ROOT_DOMAIN_URI + "/static/images/emails",
    }

    def render_templates():
        _email_subject = loader.render_to_string(template_prefix + ".subject.html", context=context).strip().replace(
            "\n", "")
        
        _html_message = loader.render_to_string(template_prefix + ".html", context)

        return _html_message, _email_subject
    
    html_message, email_subject = render_templates()

    envelope_from = settings.DEFAULT_FROM_EMAIL
    mail = EmailMessage(html_message, email_subject, envelope_from, to_emails)


def send_email(template_prefix, to_user_ids=None, to_emails=None, context={}, tenant=None, request=None):
    mail = build_email(template_prefix,
                       to_user_ids=to_user_ids,
                       to_emails=to_emails,
                       context=context,
                       tenant=tenant)
    
    mail.content_subtype = "html" # type: ignore
    mail.send(fail_silently=False) # type: ignore


def send_confirm_registration_email(email, activation_url, building=None):
    send_email(
        "email/confirm_registration",
        to_emails=[email],
        context={
            "activate_url": activation_url,
        }
    )