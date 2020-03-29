from django.contrib import admin
from profiles_api import models


admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)


class UserAdmin(BaseUserManager, UserAdmin):
    def create_user(self, email, name, password=None, **extra_fields):
        # Create a new user profile
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)

        user = User(
            email=email, is_staff=False, is_active=True,
            is_superuser=False,
        )

        #save the password here:
        user.set_password(password)
        user = self.model(email=email, **extra_fields)
        user.save(using=self._db)

        return user
