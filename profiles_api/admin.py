from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from profiles_api import models

class UserProfileAdmin(UserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal Info'), {'fields': ('name',)}),
        (
            ('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.ProfileFeedItem)
