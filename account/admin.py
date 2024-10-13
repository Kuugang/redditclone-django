from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'birth_date', 'avatar', 'about', 'updated_at')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
admin.site.register(User, UserAdmin)