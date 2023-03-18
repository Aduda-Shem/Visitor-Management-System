from django.urls import path
from django.views.generic import TemplateView
from .views import login, DashboardView, Company, addcompany, addsecurity, CarView, NoticeBoard, Visitors, Security, PasswordChange

# from company.import add_company

urlpatterns = [
    path("", DashboardView.as_view(), name='dashboard'),
    path("login", login, name="login"),
    # path("", )
    # path("add-company", add_company, name="add-company"),
    path('companies', Company.as_view(), name='company'),
     path('add-company', addcompany, name='add-company'),
    path('add-security', addsecurity, name='add-security'),
    path('vehicles', CarView.as_view(), name='vehicles'),
    path('notice-board', NoticeBoard.as_view(), name='noticeboard'),
    path('visitors', Visitors.as_view(), name='visitors'),
    path('security', Security.as_view(), name='security'),
    path('changepassword', PasswordChange.as_view(), name='pass_change'),

]