from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal

from djgeojson.fields import PointField

# Create your models here.
class Attendance(models.Model):
    employee = models.ForeignKey('user.AuthUser', on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField(auto_now_add=False, default=timezone.now)
    checkin_time = models.TimeField(null=True, blank=True)
    checkout_time = models.TimeField(null=True, blank=True)
    working_hours = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    checkin_location = PointField(null=True, blank=True)
    checkout_location = PointField(null=True, blank=True)
    checkin_devices = models.CharField(max_length=100, null=True, blank=True)
    checkout_devices = models.CharField(max_length=100, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date}"
    