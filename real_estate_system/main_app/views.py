# views.py
from django.shortcuts import render, redirect ,get_object_or_404
from .forms import *
from .models import *
from django.http import FileResponse
import os
from django.conf import settings


# main_app/views.py
# main_app/views.py
def home_page(request):
    return render(request, 'home.html')
# نفس التعديل لبقية الدوال

def site_list(request):
    sites = Site.objects.all()
    return render(request, 'site_list.html', {'sites': sites})


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

def rental_unit_list(request):
    units = RentalUnit.objects.all()
    return render(request, 'rental_unit_list.html', {'units': units})

def tenant_list(request):
    tenants = Tenant.objects.all()
    return render(request, 'tenant_list.html', {'tenants': tenants})

def contract_list(request):
    contracts = Contract.objects.all()
    return render(request, 'contract_list.html', {'contracts': contracts})

def add_site(request):
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('site_list')
    else:
        form = SiteForm()
    return render(request, 'form_template.html', {'form': form, 'title': 'إضافة موقع جديد'})

# إنشاء دوال مماثلة لـ add_rental_unit, add_tenant, add_contract


def add_rental_unit(request):
    if request.method == 'POST':
        form = RentalUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rental_unit_list')
    else:
        form = RentalUnitForm()
    return render(request, 'form_template.html', {'form': form, 'title': 'إضافة عين مؤجرة'})

def add_tenant(request):
    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm()
    return render(request, 'form_template.html', {'form': form, 'title': 'إضافة مستأجر'})

# دوال التعديل والحذف والعرض للمستأجرين
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









def add_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contract_list')
    else:
        form = ContractForm()
    return render(request, 'form_template.html', {'form': form, 'title': 'إضافة عقد'})


def view_file(request, file_path):
    """عرض الملفات المرفقة (PDF/صور)"""
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    return FileResponse(open(full_path, 'rb'), content_type='application/octet-stream')