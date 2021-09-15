from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'confirmation_code',
        'last_name',
        'bio',
        'role'
    )


admin.site.register(User, UserAdmin)
