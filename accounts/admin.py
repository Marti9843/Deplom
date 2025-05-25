from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from .forms import RegisterForm


class CustomUserAdmin(UserAdmin):
    form = RegisterForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('last_name', 'first_name')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональна інформація', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Дозволи', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важливі дати', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)