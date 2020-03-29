from django.contrib import admin
from profiles_api import models

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users import models

admin.site.register(models.MyUser, UserAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)
