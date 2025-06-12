from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from nepali_datetime_field.models import NepaliDateField

from leave.models import JobType
from utils.enums import GENDER
from utils.enums import MARITAL_STATUS
from utils.enums import RELIGION

# Create your models here.
class AuthUser(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True)

    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    username = models.CharField(max_length=150, unique=True, blank=False)
    email = models.EmailField(verbose_name='Official email', unique=True, blank=False)

    def full_name(self):
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return ' '.join(part for part in parts if part)
    
    @property
    def attendance_status_button(self):
        todays_attendance = self.attendance.filter(
            # date=timezone.localdate()
            date=timezone.now()
        )
        if todays_attendance.exists():
            # if todays_attendance.first().status == "CheckedOut":
            #     return "Already CheckedIn"
            # elif todays_attendance.first().status == "PaidLeave" or todays_attendance.first().status == "UnpaidLeave":
            #     return "Leave"
            # elif todays_attendance.first().status == "RoasterLeave":
            #     return "Roaster Leave"
            # else:
            #     return "CheckOut"

            if todays_attendance.first().checkin_time and not todays_attendance.first().checkout_time:
                return "CheckOut"
            elif todays_attendance.first().checkout_time:
                return "Already CheckedOut"
        else:
            return "CheckIn"  

    def __str__(self):
        return self.username
    
    
class Profile(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    

    user = models.OneToOneField(AuthUser, related_name='profile', on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(null=True, verbose_name='Date of birth')
    gender = models.CharField(max_length=1, choices=GENDER, default='F')
    religion = models.CharField(max_length=50, choices=RELIGION, default='H')
    mobile_number = models.CharField(max_length=15, blank=True, null=True)      
    personal_email = models.EmailField(blank=True, null=True, verbose_name='Personal email')
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS, null=True, blank=True)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS, default="S")

class WorkingDetail(models.Model):
    employee = models.OneToOneField(AuthUser, related_name='working_detail', on_delete=models.CASCADE)
    shift = models.ForeignKey('roster.Shift', related_name='shift', on_delete=models.SET_NULL, null=True)
    job_type = models.CharField(choices=JobType.choices, default=JobType.PROBATION, verbose_name="Job Type")
    joining_date = models.DateField(null=True, verbose_name="Joining Date")
    department = models.ForeignKey('department.Department', related_name='department', on_delete=models.SET_NULL, null=True)


  


