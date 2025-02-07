from django.core.management.base import BaseCommand
from main_app.models import Ejar

class Command(BaseCommand):
    help = 'حذف جميع البيانات من جدول Ejar'

    def handle(self, *args, **kwargs):
        # حذف جميع السجلات
        Ejar.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('تم حذف جميع البيانات من جدول Ejar'))
