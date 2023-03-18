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


    class Meta:
        model = TenantUser
        fields = ['email', 'full_name', 'phone_number']


class TenantSetupForm(forms.ModelForm):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    telephone = forms.CharField(required=False)
    nature_of_business = forms.ChoiceField(choices=BUILDING_CHOICES)
    slug = forms.CharField(required=False)
    physical_address = forms.CharField(required=False)
    class Meta:
        model = Building
        fields = ['name', 'email', 'telephone', 'nature_of_business', 'slug','physical_address' ]
