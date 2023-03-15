from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.test import Client
from django.views import View
from django.db import connection
from django.contrib.postgres.search import SearchVector
from tenant_schemas.utils import tenant_context, schema_context
from public.users.models import TenantUser

from public.building.models import Building, Domain
# from tenant_schemas.utils import tenant_context

from django_tenants.utils import get_tenant_model




import urllib.parse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.db.transaction import atomic
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django_tenants.utils import get_tenant_model
from tenant_users.tenants.tasks import provision_tenant
from public.core.utils import send_confirm_registration_email

from public.forms import RegistrationForm,TenantSetupForm
from public.users.models import TenantUser
from django.views.generic import TemplateView

UserProfile = get_user_model()


# class BuildingRegisterView(TemplateView):
#     form = TenantSetupForm
#     template_name = "users/building-register.html"


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
            print(user.save())
            # send_confirm_registration_email(user, )
            return redirect(reverse("building-register"))
        return self.render(request)

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
            domain.name=str(instance.name)
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

