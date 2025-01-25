# models.py
from django.db import models
from dateutil.relativedelta import relativedelta

class Site(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    additional_data = models.TextField(blank=True)

    def __str__(self):
        return self.name

class RentalUnit(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='rental_units')
    name = models.CharField(max_length=200)
    electricity_meter = models.CharField(max_length=50)
    water_meter = models.CharField(max_length=50)
    area = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.site}"

class Tenant(models.Model):
    TENANT_TYPES = (
        ('company', 'شركة'),
        ('institution', 'مؤسسة'),
        ('individual', 'فرد'),
    )
    
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TENANT_TYPES)
    id_number = models.CharField(max_length=20)
    id_issue_date = models.DateField()
    phone = models.CharField(max_length=20)
    id_copy = models.FileField(upload_to='tenants/id/')
    postal_number_copy = models.FileField(upload_to='tenants/postal/')

    def __str__(self):
        return self.name

class Contract(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    rental_unit = models.ForeignKey(RentalUnit, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    start_date = models.DateField()
    duration_months = models.IntegerField()
    end_date = models.DateField(blank=True)
    contract_file = models.FileField(upload_to='contracts/')

    def save(self, *args, **kwargs):
        # Calculate end date automatically
        self.end_date = self.start_date + relativedelta(months=+self.duration_months)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tenant} - {self.rental_unit}"