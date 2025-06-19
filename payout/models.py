from django.db import models

from user.models import AuthUser
from utils.enums import NepaliMonthList

# Create your models here.
class SalaryType(models.Model):
    name = models.CharField(unique=True, max_length=50)
    # is_taxable = models.BooleanField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True, related_name='salary_type_created_by')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Salary Type'
        verbose_name_plural = 'Salary Types'

class SalaryRelease(models.Model):
    SALARY_STATUS = [
        ('Released', 'Released'),
        ('On hold', 'On hold'),
        ('On hold release', 'On hold release')
    ]

    employee = models.ForeignKey('user.AuthUser', on_delete=models.CASCADE, related_name='salary_release_employee')
    salary_type = models.ForeignKey(SalaryType, on_delete=models.CASCADE, related_name='salary_release_salary_type', verbose_name='Salary Type')
    start_date = models.DateField(null=True,blank=True, verbose_name='Start Date')
    end_date = models.DateField(null=True,blank=True, verbose_name='End Date')
    fiscal_year = models.ForeignKey('fiscal_year.FiscalYear', on_delete=models.CASCADE, related_name='salary_release_fiscal_year', verbose_name='Fiscal Year')
    month = models.IntegerField(choices=NepaliMonthList, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_product = models.PositiveIntegerField(verbose_name='No of Product', blank=True, null=True, default=0)
    rate = models.DecimalField(max_digits=8, decimal_places=2, blank= True, null=True,default=0)
    # tax = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], blank=True, null=True, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0, verbose_name='Net Amount')
    status = models.CharField(max_length=20, choices = SALARY_STATUS, null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True, related_name='salary_release_created_by')
    updated_by = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True, related_name='salary_release_updated_by')

    def __str__(self):
        return f"{self.salary_type.name} - {self.month}"


class PayoutInterval(models.Model):
    name = models.CharField(unique=True, max_length=50)
    day = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True, related_name='payout_interval_created_by')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Payout Interval'
        verbose_name_plural = 'Payout Intervals'
