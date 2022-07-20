from django.contrib import admin
from django.contrib.auth.models import  User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
        list_display = ("email", "first_name", "last_name")
        fieldsets = (
            (None, {'fields': ('email', 'first_name', "last_name", 'password')}),
            ('Permissions', {'fields': ('is_superuser', 'last_login')}),
        )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)