# forms.py
from django import forms
from .models import *


# دالة لتطبيق السمات العامة على الحقول
def apply_widgets_attrs(form):
    for field_name, field in form.fields.items():
        # إضافة سمات أساسية لجميع الحقول
        field.widget.attrs.update({
            'class': 'form-control',  # إضافة فئة CSS موحدة
            'placeholder': f'أدخل {field.label} هنا',  # نص مساعدة داخل الحقل
            'id': f'field_{field_name}',  # تعيين id بشكل ديناميكي بناءً على اسم الحقل
            'required': 'required',  # جعل الحقل إلزامي
            'autocomplete': 'off',  # تعطيل الإكمال التلقائي
            'aria-label': f'Field for {field.label}',  # تحسين الوصول (accessibility)
        })

        # تخصيص الحقول التي هي نوع Textarea
        if isinstance(field.widget, forms.Textarea):
            field.widget.attrs.update({
                'rows': 4,  # تحديد عدد الصفوف لحقل النص
            })
        
        # تخصيص الحقول التي هي نوع DateInput
        elif isinstance(field.widget, forms.DateInput):
            field.widget.attrs.update({
                'type': 'date',  # تحديد نوع الإدخال كـ "تاريخ"
            })
        
        # تخصيص الحقول التي هي نوع NumberInput
        elif isinstance(field.widget, forms.NumberInput):
            field.widget.attrs.update({
                'type': 'number',  # تحديد نوع الإدخال كـ "رقم"
            })

        # تخصيص الحقول التي هي نوع TextInput
        elif isinstance(field.widget, forms.TextInput):
            field.widget.attrs.update({
                'type': 'text',  # تحديد نوع الإدخال كـ "نص"
            })

        # تخصيص سمات خاصة لبعض الحقول مثل "amount_in_words" (قراءة فقط)
        if field_name == 'amount_in_words':
            field.widget.attrs.update({
                'readonly': 'readonly',  # جعل الحقل للقراءة فقط
            })

        # تخصيص بعض الحقول الأخرى
        if field_name == 'amount':
            field.widget.attrs.update({
                'onblur': 'calculateAmount()',  # إضافة حدث "onblur" لحقل المبلغ
            })



class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        # استدعاء __init__ من parent class بشكل صحيح
        super().__init__(*args, **kwargs)
        
        # الآن يمكنك إضافة السمات الخاصة بك
        apply_widgets_attrs(self)
    
        

class RentalUnitForm(forms.ModelForm):
    class Meta:
        model = RentalUnit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # استدعاء __init__ من parent class بشكل صحيح
        super().__init__(*args, **kwargs)
        
        # الآن يمكنك إضافة السمات الخاصة بك
        apply_widgets_attrs(self)



class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'
        widgets = {
            'type': forms.Select(choices=Tenant.TENANT_TYPES),
            'id_issue_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # استدعاء __init__ من parent class بشكل صحيح
        super().__init__(*args, **kwargs)
        
        # الآن يمكنك إضافة السمات الخاصة بك
        apply_widgets_attrs(self)




class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['site', 'rental_unit', 'tenant', 'start_date', 'duration_months', 'contract_file']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

            
        # الآن يمكنك إضافة السمات الخاصة بك
       

    def __init__(self, *args, **kwargs):
        site_id = kwargs.pop('site_id', None)
        super().__init__(*args, **kwargs)
        apply_widgets_attrs(self)
        
        # تصفية الوحدات المؤجرة بناءً على الموقع المحدد
        if site_id:
            self.fields['rental_unit'].queryset = RentalUnit.objects.filter(site_id=site_id)
        else:
            self.fields['rental_unit'].queryset = RentalUnit.objects.none()
        
        # إعداد قائمة المستأجرين
        self.fields['tenant'].queryset = Tenant.objects.all()



class ejarForm(forms.ModelForm):
    class Meta:
        model = Ejar
        fields = '__all__'



