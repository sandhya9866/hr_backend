from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on')
    search_fields = ('name',)
    filter_horizontal = ('department_head',)
