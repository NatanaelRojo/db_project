from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    #add_form = CustomUserCreationForm
    #form = CustomUserChangeForm
    #model = CustomUser
    list_display = ["email", "username", "phone_number", "creation_date",]
    fieldsets = (
        ("Personal Info", {
            "fields": (
                "first_name",
                "last_name",
                "username",
                "email",
                "password",
                "phone_number",
            )
        }),
        ("Permissions", {
            "fields": (
                "user_permissions",
                "is_staff",
                "is_active",
                "is_superuser",
            )
        })
    )


#admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomUser, CustomUserAdmin)