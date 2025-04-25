from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import AuthUser

class AuthUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "middle_name",
            ),
        }),
    )
    
# class ProfileAdmin()

# Register your models here.
admin.site.register(AuthUser, AuthUserAdmin)