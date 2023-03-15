from django.contrib.auth.tokens import default_token_generator

def send_confirm_registration_email(email, context):
    token = token_generator.make_token