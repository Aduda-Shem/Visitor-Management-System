from django.shortcuts import redirect, render
from .forms import TenantUserLoginForm as LoginForm
from django.contrib.auth import authenticate, login as auth_login
from django.views.generic import TemplateView


# Create your views here.
def login(request):
    if request.method == "POST":
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        print('user',user)
        if user is None:
            return render (request, 'users/user-login.html', {'form': LoginForm(), 'error':'email and password do not match'})
        else:
            auth_login(request, user)

            return redirect('/')
    else:
        return render(request, 'users/user-login.html', {'form': LoginForm()})

class DashboardView(TemplateView):
    template_name = "building/dashboard.html"

class Company(TemplateView):
    template_name = "company/company.html"
class CarView(TemplateView):
    template_name = "building/vehicles.html"

class NoticeBoard(TemplateView):
    template_name = "building/notices.html"

class Visitors(TemplateView):
    template_name = "visitors/visitors.html"

class Security(TemplateView):
    template_name = "security/security.html"


def addsecurity(request):
     return render(request, template_name="security/addsecurity.html")

def addcompany(request):
    return render(request, template_name="company/add-company.html")
class PasswordChange(TemplateView):
    template_name = "users/change-password.html"