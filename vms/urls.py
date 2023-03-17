from django.urls import path
from django.views.generic import TemplateView
from .views import login
# from company.views import add_company

urlpatterns = [
    path("login", login, name="login"),
    # path("add-company", add_company, name="add-company")
]