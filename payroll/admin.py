from django.contrib import admin
from .models import SalaryType

@admin.register(SalaryType)
class SalaryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on', 'created_by')
    search_fields = ('name',)
    list_filter = ('created_on',)
    readonly_fields = ('created_on', 'created_by')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
