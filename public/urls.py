from django.urls import path
from django.views.generic import TemplateView

from public.views import SignupView, TenantSetupView
from public.building import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name='index'),
    path("signup", SignupView.as_view(), name="signup"),
    path("building_register", TenantSetupView.as_view(), name='building-register'),
    path('add-company', views.addcompany, name='add-company'),
    path('add-security', views.addsecurity, name='add-security'),
    path('vehicles', views.CarView.as_view(), name='vehicles'),
    path('notice-board', views.NoticeBoard.as_view(), name='noticeboard'),
    path('visitors', views.Visitors.as_view(), name='visitors'),
    path('security', views.Security.as_view(), name='security'),
    path('companies', views.Company.as_view(), name='company'),
    path('changepassword', views.PasswordChange.as_view(), name='pass_change'),
    
]