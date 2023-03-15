from django import forms
from public.users.models import TenantUser


class TenantUserLoginForm(forms.ModelForm):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    
    class Meta:
        model = TenantUser #or whatever object
        fields = [ 'email', 'password']