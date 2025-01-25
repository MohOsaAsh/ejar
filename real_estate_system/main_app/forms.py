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
        fields = ['site', 'rental_unit', 'tenant', 'start_date', 'duration_months', 'contract_file']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        site_id = kwargs.pop('site_id', None)
        super().__init__(*args, **kwargs)
        
        # تصفية الوحدات المؤجرة بناءً على الموقع المحدد
        if site_id:
            self.fields['rental_unit'].queryset = RentalUnit.objects.filter(site_id=site_id)
        else:
            self.fields['rental_unit'].queryset = RentalUnit.objects.none()
        
        # إعداد قائمة المستأجرين
        self.fields['tenant'].queryset = Tenant.objects.all()



