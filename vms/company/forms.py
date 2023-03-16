from django import forms 
from .models import Company

# Create here
class AddCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['company_name', 'email', 'telephone_number', 'building_floor', 'description']