from django.db import models
from utils.enums import ACTIVE_INACTIVE, YesNoList

class FiscalYear(models.Model):
    fiscal_year = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(default='active', choices=ACTIVE_INACTIVE)
    is_current = models.BooleanField(default=False, choices=YesNoList)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    @classmethod
    def active_fiscal_year_list(cls):
        return cls.objects.filter(status='active').order_by('-id')
    
    @classmethod
    def current_fiscal_year(cls):
        return cls.objects.filter(is_current=True, status='active').first()

    def __str__(self):
        return self.fiscal_year
