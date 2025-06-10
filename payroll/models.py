from django.db import models

from user.models import AuthUser

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