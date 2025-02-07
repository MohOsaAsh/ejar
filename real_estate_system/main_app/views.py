# views.py
from django.shortcuts import render, redirect ,get_object_or_404
from .forms import *
from .models import *
from django.http import FileResponse
import os
from django.conf import settings


# main_app/views.py
def home_page(request):
    return render(request, 'home.html')
# نفس التعديل لبقية الدوال


#############
# إدارة المواقع #
#############

def site_list(request):
    sites = Site.objects.all()
    return render(request, 'site_list.html', {'sites': sites})

def add_site(request):
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('site_list')
    else:
        form = SiteForm()
    return render(request, 'form_template.html', {'form': form, 'title': 'إضافة موقع جديد'})

def view_site(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    return render(request, 'view_site.html', {'site': site})


def edit_site(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    if request.method == 'POST':
        form = SiteForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            return redirect('site_list')
    else:
        form = SiteForm(instance=site)
    return render(request, 'form_template.html', {'form': form, 'title': 'تعديل موقع'})

def delete_site(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    site.delete()
    return redirect('site_list')


#####################
# إدارة العين المؤجرة #
#####################
# def rental_unit_list(request):
#     """عرض قائمة جميع الوحدات المؤجرة"""
#     units = RentalUnit.objects.all()
#     return render(request, 'rental_unit_list.html', {'units': units})

def rental_unit_list(request):
    # الحصول على معايير التصفية من الـ URL
    site_id = request.GET.get('site')
    name = request.GET.get('name')

    # تصفية الوحدات
    units = RentalUnit.objects.all()
    if site_id:
        units = units.filter(site_id=site_id)
    if name:
        units = units.filter(name__icontains=name)  # بحث غير حساس لحالة الأحرف

    # جلب جميع المواقع لعرضها في الفلتر
    sites = Site.objects.all()

    return render(request, 'rental_unit_list.html', {
        'units': units,
        'sites': sites,
    })



def add_rental_unit(request):
    """إضافة وحدة مؤجرة جديدة"""
    if request.method == 'POST':
        form = RentalUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rental_unit_list')
    else:
        form = RentalUnitForm()
    return render(request, 'form_template.html', {
        'form': form,
        'title': 'إضافة عين مؤجرة'
    })

def view_unit(request, unit_id):
    """عرض تفاصيل وحدة مؤجرة"""
    unit = get_object_or_404(RentalUnit, pk=unit_id)
    return render(request, 'view_unit.html', {'unit': unit})

def edit_unit(request, unit_id):
    """تعديل بيانات وحدة مؤجرة"""
    unit = get_object_or_404(RentalUnit, pk=unit_id)
    if request.method == 'POST':
        form = RentalUnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('rental_unit_list')
    else:
        form = RentalUnitForm(instance=unit)
    return render(request, 'form_template.html', {
        'form': form,
        'title': 'تعديل عين مؤجرة'
    })

def delete_unit(request, unit_id):
    """حذف وحدة مؤجرة من النظام"""
    unit = get_object_or_404(RentalUnit, pk=unit_id)
    unit.delete()
    return redirect('rental_unit_list')



###################
# إدارة المستأجرين #
###################

# def tenant_list(request):
#     tenants = Tenant.objects.all()
#     return render(request, 'tenant_list.html', {'tenants': tenants})

def tenant_list(request):
    # الحصول على معايير التصفية من الـ URL
    name = request.GET.get('name')
    city = request.GET.get('city')

    # تصفية المستأجرين
    tenants = Tenant.objects.all()
    if name:
        tenants = tenants.filter(name__icontains=name)  # بحث غير حساس لحالة الأحرف
    if city:
        tenants = tenants.filter(city__icontains=city)  # يمكنك تغييرها إلى "iexact" للبحث الدقيق

    # جلب جميع المدن المميزة لعرضها في الفلتر (اختياري)
    cities = Tenant.objects.values_list('city', flat=True).distinct()

    return render(request, 'tenant_list.html', {
        'tenants': tenants,
        'cities': cities,
    })

def add_tenant(request):
    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm()
    return render(request, 'form_template.html', {'form': form, 'title': 'إضافة مستأجر'})


def view_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    return render(request, 'view_tenant.html', {'tenant': tenant})

def edit_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant)
    return render(request, 'form_template.html', {'form': form, 'title': 'تعديل مستأجر'})

def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    tenant.delete()
    return redirect('tenant_list')


################
# إدارة العقود #
################

def contract_list(request):
    contracts = Contract.objects.all()
    return render(request, 'contract_list.html', {'contracts': contracts})

def add_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contract_list')
    else:
        form = ContractForm()
    return render(request, 'form_template.html', {'form': form, 'title': 'إضافة عقد'})

def view_contract(request, contract_id):
    """عرض تفاصيل عقد معين"""
    contract = get_object_or_404(Contract, pk=contract_id)
    return render(request, 'view_contract.html', {'contract': contract})

def edit_contract(request, contract_id):
    """تعديل بيانات عقد موجود"""
    contract = get_object_or_404(Contract, pk=contract_id)
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES, instance=contract)
        if form.is_valid():
            form.save()
            return redirect('contract_list')
    else:
        form = ContractForm(instance=contract)
    return render(request, 'form_template.html', {
        'form': form,
        'title': 'تعديل عقد'
    })

def delete_contract(request, contract_id):
    """حذف عقد من النظام"""
    contract = get_object_or_404(Contract, pk=contract_id)
    contract.delete()
    return redirect('contract_list')

####################
# إدارة الملفات المرفقة #
####################

def view_file(request, file_path):
    """عرض الملفات المرفقة (PDF/صور)"""
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    return FileResponse(open(full_path, 'rb'), content_type='application/octet-stream')




####################
# إدارة عقود  الايجار #
####################



def ejar_list(request):
    ejars = Ejar.objects.all()
    return render(request, 'ejar_list.html', {'ejars': ejars})



    """حذف عقد من النظام"""

def delete_ejar(request, ejar_id):
    ejar = get_object_or_404(Ejar, pk=ejar_id)
    ejar.delete()
    return redirect('ejar_list')


def view_ejar(request, ejar_id):
    """عرض تفاصيل وحدة مؤجرة"""
    ejar = get_object_or_404(Ejar, pk=ejar_id)
    return render(request, 'view_ejar.html', {'ejar': ejar})

def edit_ejar(request, ejar_id):
    """تعديل بيانات وحدة مؤجرة"""
    ejar = get_object_or_404(Ejar, pk=ejar_id)
    if request.method == 'POST':
        form = ejarForm(request.POST, instance=ejar)
        if form.is_valid():
            form.save()
            return redirect('ejar_list')
    else:
        form = ejarForm(instance=ejar)
    return render(request, 'form_template.html', {
        'form': form,
        'title': 'تعديل عين مؤجرة'
    })
def add_ejar(request):
    if request.method == 'POST':
        form = ejarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ejar_list')
    else:
        form = ejarForm()
    return render(request, 'form_template.html', {'form': form, 'title': 'إضافة عقد'})
