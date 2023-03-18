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
