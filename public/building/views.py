from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from public.forms import RegistrationForm, TenantSetupForm

from public.views import SignupView, TenantSetupView
from formtools.wizard.views import SessionWizardView




#our views go here

class CarView(TemplateView):
    template_name = "building/vehicles.html"

class NoticeBoard(TemplateView):
    template_name = "building/notices.html"

class Visitors(TemplateView):
    template_name = "visitors/visitors.html"

class Security(TemplateView):
    template_name = "security/security.html"

class Company(TemplateView):
    template_name = "company/company.html"

def addsecurity(request):
     return render(request, template_name="security/addsecurity.html")

def addcompany(request):
    return render(request, template_name="company/add-company.html")
class PasswordChange(TemplateView):
    template_name = "users/change-password.html"

def index(request):
    return render(request, template_name="building/index.html")


    