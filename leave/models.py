from django.db import models
from utils.enums import ACTIVE_INACTIVE, GENDER
from utils.enums import MARITAL_STATUS
from nepali_datetime_field.models import NepaliDateField

class LeaveTypeOptions(models.TextChoices):
    PAID = 'paid', 'Paid'
    UNPAID = 'unpaid', 'Unpaid'
    ROSTER = 'roaster', 'Roster'

class HalfLeaveType(models.TextChoices):
    FIRST_HALF = 'first_half', 'First Half'
    SECOND_HALF = 'second_half', 'Second Half'

class JobType(models.TextChoices):
    ALL = 'all', 'All'
    PERMANENT = 'permanent', 'Permanent'
    CONTRACT = 'contract', 'Contract'
    PROBATION = 'probation', 'Probation'

class LeaveType(models.Model):
    fiscal_year = models.ForeignKey('fiscal_year.FiscalYear', on_delete=models.CASCADE, related_name='leave_type_fiscal_year', null=True)
    name = models.CharField(max_length=100, verbose_name="Title")
    code = models.CharField(max_length=10, blank=True, null=True)
    leave_type = models.CharField(max_length=50, choices=LeaveTypeOptions.choices, default=LeaveTypeOptions.PAID, verbose_name="Type")
    gender = models.CharField(max_length=1, choices=GENDER, default='A')
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS, default="A")
    number_of_days = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    show_on_employee = models.BooleanField(default=True, verbose_name="Display on Employee?")
    prorata_status = models.BooleanField(default=False, verbose_name="Enable Prorata?")          
    encashable_status = models.BooleanField(default=False, verbose_name="Enable Encashable?")
    half_leave_status = models.BooleanField(default=False, verbose_name="Enable Half Leave?")
    half_leave_type = models.CharField(max_length=50, choices=HalfLeaveType.choices, default=HalfLeaveType.FIRST_HALF)
    carry_forward_status = models.BooleanField(default=False, verbose_name="Enable Carry Forward?")
    sandwich_rule_status = models.BooleanField(default=False, verbose_name="Enable Sandwich Rule?")     
    pre_inform_days = models.IntegerField(null=True, blank=True, verbose_name="Leave request should be submitted before (in days)")
    max_per_day_leave = models.IntegerField(null=True, blank=True, verbose_name="Maximum number of days per request")
    status = models.CharField(default='active', choices=ACTIVE_INACTIVE)
    job_type = models.CharField(max_length=50, choices=JobType.choices, default=JobType.ALL, verbose_name="Job Type")
    created_by = models.ForeignKey('user.AuthUser', on_delete=models.CASCADE, related_name='leave_type_created_by', null=True)
    updated_by = models.ForeignKey('user.AuthUser', on_delete=models.CASCADE, related_name='leave_type_updated_by', null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class EmployeeLeave(models.Model):
    employee = models.ForeignKey('user.AuthUser', on_delete=models.CASCADE, related_name='employee_leave_employee')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='employee_leave_type')
    total_leave = models.FloatField()
    leave_taken = models.FloatField()
    leave_remaining = models.FloatField()
    created_by = models.ForeignKey('user.AuthUser', on_delete=models.CASCADE, related_name='employee_leave_created_by', null=True)
    updated_by = models.ForeignKey('user.AuthUser', on_delete=models.CASCADE, related_name='employee_leave_updated_by', null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee} - {self.leave_type} - {self.leave_remaining} days"


class Leave(models.Model):
    LEAVE_STATUS = [
        ('Applied','Applied'),
        ('Verified','Verified'),
        ('Declined','Declined'),
        ('Approved','Approved'),
    ]

    employee = models.ForeignKey('user.AuthUser', on_delete=models.CASCADE, related_name='employee_leave')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='leave_type_leave')
    start_date = NepaliDateField()
    end_date = NepaliDateField()
    no_of_days = models.PositiveIntegerField(default=0)
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(choices=LEAVE_STATUS,default="Applied")
    created_by = models.ForeignKey('user.AuthUser', on_delete=models.CASCADE, related_name='leave_created_by', null=True)
    updated_by = models.ForeignKey('user.AuthUser', on_delete=models.CASCADE, related_name='leave_updated_by', null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee} - {self.leave_type} - {self.start_date} to {self.end_date}"

