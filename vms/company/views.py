from django.shortcuts import render, redirect, get_object_or_404

from .models import Company
from .forms import AddCompanyForm
from public.users.models import TenantUser
from public.building.models import Building

# Create your views here.
def add_company(request):
    # user = TenantUser
    current_user = request.user
    form = AddCompanyForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            return redirect ('/index')
        else:
            form = AddCompanyForm()
    return render(request, 'company/company.html', {'form':form})