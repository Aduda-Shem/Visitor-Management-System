from urllib import request
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.test import Client
from django.views import View
from django.views.generic import TemplateView, View, UpdateView
from django.db import connection
from django.db.transaction import atomic
from django.urls import reverse, reverse_lazy
from django.contrib.postgres.search import SearchVector
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django_tenants.utils import get_tenant_model
from django.core.mail import send_mail, EmailMessage

from django.contrib.auth.models import User

from tenant_schemas.utils import tenant_context, schema_context
from tenant_users.tenants.tasks import provision_tenant
# from tenant_schemas.utils import tenant_context

from formtools.wizard.views import SessionWizardView

from public.users.models import TenantUser
from public.building.models import Building, Domain
from public.core.utils import send_confirm_registration_email
from public.forms import RegistrationForm,TenantSetupForm
from public.tokens import account_activation_token

import urllib.parse

# Create here
UserProfile = get_user_model()

class SignupView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.form = None

    def render(self, request):
        context = {
            "form": self.form,
            "MAX_PASSWORD_LENGTH": str(self.form.MAX_PASSWORD_LENGTH)
        }
        return render(request, "users/user-register.html", context)

    def get(self, request, *args, **kwargs):
        self.form = RegistrationForm()
        return self.render(request)

    def post(self, request, *args, **kwargs):
        self.form = RegistrationForm(request.POST)
        if self.form.is_valid():
            # email = self.form.cleaned_data["email"]
            # full_name = self.form.cleaned_data["full_name"]
            # phone_number = self.form.cleaned_data["phone_number"]
            # national_id = self.form.cleaned_data["national_id"]
            password = self.form.cleaned_data['password']
            user = self.form.save(commit=False)
            user.set_password(password)
            user.save()
            
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('email/account_activation_email.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            # user.email_user(subject, message)
            send_mail(
                subject, message, '',[user.email], fail_silently=False
            )
            messages.success(request, ('Please confirm your email to complete the registration process'))
            
            return HttpResponse('Succcess!!!')    
            # return redirect(reverse("building-register"))        
        return self.render(request)


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = TenantUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, TenantUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, ('Your account has been confirmed.'))
            return HttpResponse('Done!!!')
            # return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return HttpResponse('Unsuccessful :(')
            # return redirect('home')

class TenantSetupView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.form = None

    def render(self, request):
        context = {
            "form": self.form,
        }
        return render(request, "users/building-register.html", context)
    def get(self, request):
        form = TenantSetupForm()
        return render(request, "users/building-register.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        self.form = TenantSetupForm(request.POST)
        form = self.form
        # print(form.is_valid())
        if self.form.is_valid():
            instance = Building()
            instance.name = form.cleaned_data['name']
            instance.website = form.cleaned_data['slug']
            instance.telephone = form.cleaned_data['telephone']
            instance.email = form.cleaned_data['email']
            instance.physical_address = form.cleaned_data['physical_address']
            instance.nature_of_business = form.cleaned_data['nature_of_business']
            instance.owner=TenantUser.objects.first()
            instance.schema_name=str(instance.name)

            # provision_tenant(instance.name, instance.website, instance.email, is_staff=True)
            instance.save()
            print(instance)

            domain=Domain()
            domain.domain=f"{instance.name}.localhost"
            

            # tenant = tenant_context(domain_url=domain, schema_name=str(instance.building_name), name=instance.building_name)
            # tenant.save()
            tm = get_tenant_model()
            tenant = tm.objects.get(schema_name=instance.schema_name)
            print(tenant)

            domain.tenant=tenant
            domain.save()
            print(domain)


            with schema_context(instance.schema_name):
                instance.save()
                # redirect = f"{instance.name}.localhost:8000/login"
                redirect = "http://" + instance.name + ".localhost:8000/login"
                # print(redirect)
                return HttpResponseRedirect(redirect)
        return render(request, "users/building-register.html", {"form": form})
    
class FormWizardView(SessionWizardView):
    """View for user and tenant creation wizard"""
    template_name = "../templates/landing.html"
    form_list = [RegistrationForm, TenantSetupForm]
    def done(self, form_list, **kwargs):
        print(self.request, [form.cleaned_data for form in form_list])
        user_form=form_list[0]
        building_form=form_list[1]
        user=TenantUser()
        user.full_name=user_form.cleaned_data['full_name']
        user.phone_number=user_form.cleaned_data['phone_number']
        user.email=user_form.cleaned_data['email']
        password=TenantUser.objects.make_random_password()
        user.password=password
        user.save()


        print(user, password)

        slug=building_form.cleaned_data['slug']
        building=Building()

        building.name=building_form.cleaned_data['name']
        building.email=building_form.cleaned_data['email']
        building.nature_of_business=building_form.cleaned_data['nature_of_business']
        building.website=building_form.cleaned_data['slug']
        building.physical_address=building_form.cleaned_data['physical_address']
        building.telephone=building_form.cleaned_data['telephone']
        building.owner=user
        building.schema_name=slug
        building.save()

        domain=Domain()
        domain.domain=f"{slug}.localhost"
        

        # tenant = tenant_context(domain_url=domain, schema_name=str(instance.building_name), name=instance.building_name)
        # tenant.save()

        domain.tenant=building
        domain.save()

        email=user_form.cleaned_data['email']
        subject = 'Activate your Account'
        message = render_to_string('email/confirm_registration.html',{
            'user': user,
            'domain': f"{domain.domain}:8000/login",
            'password':password,
        })

        # user.email_user(subject, message)
        send_mail(
            subject, message, '',[email], fail_silently=False
        )
        print(message)
        messages.success(self.request, ('Please confirm your email to complete the registration process'))
            
        return render(self.request, "email/accounts_send_confirm.html")
    

