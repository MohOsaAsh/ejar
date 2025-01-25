
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

# main_app/urls.py
from django.urls import path
from . import views

urlpatterns = [

    # مسارات المواقع 
    path('sites/', views.site_list, name='site_list'),
    path('sites/add/', views.add_site, name='add_site'),
    path('sites/<int:site_id>/', views.view_site, name='view_site'),
    path('sites/<int:site_id>/edit/', views.edit_site, name='edit_site'),
    path('sites/<int:site_id>/delete/', views.delete_site, name='delete_site'),

 # مسارات العين المؤجرة
    path('units/', views.rental_unit_list, name='rental_unit_list'),
    path('units/add/', views.add_rental_unit, name='add_rental_unit'),
    path('units/<int:unit_id>/', views.view_unit, name='view_unit'),
    path('units/<int:unit_id>/edit/', views.edit_unit, name='edit_unit'),
    path('units/<int:unit_id>/delete/', views.delete_unit, name='delete_unit'),
 
# مسارات المستأجرين
    path('tenants/', views.tenant_list, name='tenant_list'),
    path('tenants/add/', views.add_tenant, name='add_tenant'),
    path('tenants/<int:tenant_id>/', views.view_tenant, name='view_tenant'),
    path('tenants/<int:tenant_id>/edit/', views.edit_tenant, name='edit_tenant'),
    path('tenants/<int:tenant_id>/delete/', views.delete_tenant, name='delete_tenant'),

   
 # مسارات العقود
    path('contracts/', views.contract_list, name='contract_list'),
    path('contracts/add/', views.add_contract, name='add_contract'),
    path('contracts/<int:contract_id>/', views.view_contract, name='view_contract'),
    path('contracts/<int:contract_id>/edit/', views.edit_contract, name='edit_contract'),
    path('contracts/<int:contract_id>/delete/', views.delete_contract, name='delete_contract'),
    
    
    path('media/view/<path:file_path>/', views.view_file, name='view_file'),
  
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
