from django.urls import path
from django.views.generic import TemplateView
from .views import login, DashboardView
# from company.views import add_company

urlpatterns = [
    path("", DashboardView.as_view(), name='dashboard'),
    path("login", login, name="login"),
    # path("", )
    # path("add-company", add_company, name="add-company")
]