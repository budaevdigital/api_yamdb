from django.contrib import admin
from .models import CustomUser


# вместо admin.site.register, используем @admin.register
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username',
                    'email', 'first_name',
                    'last_name', 'date_joined',
                    'role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name',)
    list_filter = ('is_staff', 'role')
    list_editable = ('is_staff', 'role', 'email', 'username', 'first_name',
                     'last_name', )
    readonly_fields = ('date_joined',)
    empty_value_display = '-пусто-'
