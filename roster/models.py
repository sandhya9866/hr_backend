from django.utils import timezone
from django.db import models
from user.models import AuthUser

# Create your models here.
class Shift(models.Model):
    title = models.CharField(max_length=100)
    colour = models.CharField(max_length=20, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    min_start_time = models.TimeField(null=True, blank=True)
    max_end_time = models.TimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title
    
class Roster(models.Model):
    employee = models.ForeignKey('user.AuthUser', on_delete=models.CASCADE, related_name='roster')
    date = models.DateField(default=timezone.now)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('user.AuthUser', on_delete=models.SET_NULL, blank=True, null=True, related_name='roster_created_by')
    updated_by = models.ForeignKey('user.AuthUser', on_delete=models.SET_NULL, blank=True, null=True, related_name='roster_updated_by')

    def __str__(self):
        return self.employee.username + " - " + str(self.date)
    
class RosterDetail(models.Model):
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name='roster_details')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='shift_detail')
   
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('user.AuthUser', on_delete=models.SET_NULL, blank=True, null=True, related_name='roster_detail_created_by')
    updated_by = models.ForeignKey('user.AuthUser', on_delete=models.SET_NULL, blank=True, null=True, related_name='roster_detail_updated_by')

    def __str__(self):
        return f"{self.roster.employee.username} - {self.shift.title}"
