import pandas as pd
from django.core.management.base import BaseCommand
from main_app.models import Ejar  # استبدل باسم التطبيق والموديل

class Command(BaseCommand):
    help = "Import Excel data into the database"

    def handle(self, *args, **kwargs):
        file_path = r"c:\data\data.xlsx"  # استخدم `r` لمنع مشاكل المسار
        try:
            df = pd.read_excel(file_path, dtype={"col1": str, "col3": int, "col4": str})  # تحديد أنواع البيانات
            
            # التأكد من وجود الأعمدة المطلوبة
            required_columns = {"col1", "col2", "col3", "col4", "col5", "col6"}
            if not required_columns.issubset(df.columns):
                self.stdout.write(self.style.ERROR(f"❌ الملف لا يحتوي على جميع الأعمدة المطلوبة: {required_columns - set(df.columns)}"))
                return
            
            # تحويل القيم إلى DateTime
            df["col2"] = pd.to_datetime(df["col2"], errors="coerce").dt.date
            df["col5"] = pd.to_datetime(df["col5"], errors="coerce").dt.date
            df["col6"] = pd.to_datetime(df["col6"], errors="coerce").dt.date

            # إنشاء الكائنات للإدخال إلى قاعدة البيانات
            objects = [
                Ejar(
                    conno=row["col1"],   # رقم العقد
                    dateren=row["col2"], # تاريخ التجديد
                    nameno=row["col3"],  # رقم العميل
                    name=row["col4"],    # اسم العميل
                    datestr=row["col5"], # تاريخ البدء
                    dateend=row["col6"], # تاريخ الانتهاء
                )
                for _, row in df.iterrows()
            ]

            # إدخال البيانات دفعة واحدة إلى قاعدة البيانات
            Ejar.objects.bulk_create(objects)

            self.stdout.write(self.style.SUCCESS(f"✅ تم إدخال {len(objects)} سجل بنجاح من الملف {file_path}!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ حدث خطأ أثناء استيراد البيانات: {e}"))
