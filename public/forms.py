from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

from public.building.models import Building
from public.users.models import TenantUser

User = get_user_model()

BUILDING_CHOICES = (
    ("COMMERCIAL", "COMMERCIAL"),
    ("RESIDENTIAL", "RESIDENTIAL"),
    ("FACTORY", "FACTORY"),
    
)

class RegistrationForm(forms.ModelForm):
    MAX_PASSWORD_LENGTH = 100

    email = forms.EmailField()
    full_name = forms.CharField(max_length=100)
    phone_number = forms.CharField()
    national_id = forms.CharField()

    password = forms.CharField(widget=forms.PasswordInput, max_length=MAX_PASSWORD_LENGTH)


    class Meta:
        model = TenantUser
        fields = ['email', 'full_name', 'phone_number', 'password']


class TenantSetupForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    telephone = forms.CharField(required=False)
    nature_of_business = forms.ChoiceField(choices=BUILDING_CHOICES)
    slug = forms.CharField(required=False)
    physical_address = forms.CharField(required=False)



# class BuildingForm(forms.ModelForm):
#     name = forms.CharField(max_length=30)
#     url = forms.URLField(max_length=30)
#     email = forms.EmailField(max_length=100)
#     description = forms.CharField(max_length=50, widget=forms.Textarea(),help_text='Building description!')
            
#     class Meta:
#          model = Building
#          fields = ['building_name', 'url', 'email', 'description']