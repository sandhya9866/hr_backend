from django.db import models
from utils.enums import ACTIVE_INACTIVE, YesNoList
from nepali_datetime_field.models import NepaliDateField

class FiscalYear(models.Model):
    fiscal_year = models.CharField(max_length=50)
    start_date = NepaliDateField()
    end_date = NepaliDateField()
    status = models.CharField(default='active', choices=ACTIVE_INACTIVE)
    is_current = models.BooleanField(default=False, choices=YesNoList)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    

    def __str__(self):
        return self.fiscal_year
