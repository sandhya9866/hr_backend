from django.contrib import admin

# Register your models here.
admin.site.site_header = "Leave Management System"
admin.site.site_title = "Leave Management System Admin" 
admin.site.index_title = "Welcome to Leave Management System Admin"
from .models import LeaveType, EmployeeLeave
from .models import Leave
@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_of_days', 'description', 'show_on_employee', 'prorata_status', 'encashable_status', 'half_leave_status', 'half_leave_type', 'carry_forward_status', 'sandwich_rule_status', 'pre_inform_days', 'max_per_day_leave', 'status', 'job_type')
    search_fields = ('name',)
    list_filter = ('status', 'job_type')
    ordering = ('name',)
@admin.register(EmployeeLeave)
class EmployeeLeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'total_leave', 'leave_taken', 'leave_remaining', 'is_active')
    search_fields = ('employee__username', 'leave_type__name')
    list_filter = ('is_active',)
    ordering = ('employee',)

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'no_of_days', 'reason', 'status')
    search_fields = ('employee__username', 'leave_type__name', 'reason')
    list_filter = ('status',)
    ordering = ('-created_on',)
    