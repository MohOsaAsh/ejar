# forms.py
from django import forms
from .models import *

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'additional_data': forms.Textarea(attrs={'rows': 3}),
        }

class RentalUnitForm(forms.ModelForm):
    class Meta:
        model = RentalUnit
        fields = '__all__'

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'
        widgets = {
            'type': forms.Select(choices=Tenant.TENANT_TYPES),
            'id_issue_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }