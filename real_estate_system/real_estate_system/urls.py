from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main_app import views  # أضف هذا الاستيراد

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),  # تأكد من إضافة هذا السطر
    path('sites/', include('main_app.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
