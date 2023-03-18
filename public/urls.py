from django import views
from django.urls import include, path
from django.views.generic import TemplateView 
from . import views
# from vms.company.views import add_company
from public.views import SignupView, TenantSetupView, ActivateAccount,  FormWizardView
from public.building import views

urlpatterns = [
    # path("signup", SignupView.as_view(), name="signup"),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

    path("building_register", TenantSetupView.as_view(), name='building-register'),
    path("register", FormWizardView.as_view(), name='register'), 
    path("", views.index, name='index'),
]
