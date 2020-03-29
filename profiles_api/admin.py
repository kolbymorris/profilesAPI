from django.contrib import admin
from profiles_api import models
from django.contrib.auth.admin import UserAdmin

admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)
admin.site.register(CustomUser, CustomUserAdmin)
