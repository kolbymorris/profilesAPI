from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.models import CloudinaryField



class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,)
        picture = cloudinary.config(
              cloud_name = "dxyhqk4td",
              api_key = "788725593668948",
              api_secret = "DjOsDIocexQ-ynSrHHiY_72SiM4"
            )
    class Photo(models.Model):
        ## Misc Django Fields
        create_time = models.DateTimeField(auto_now_add=True)
        title = models.CharField("Title (optional)", max_length=200, blank=True)

        ## Points to a Cloudinary image
        image = CloudinaryField('image')

        """ Informative name for model """
        def __unicode__(self):
            try:
                public_id = self.image.public_id
            except AttributeError:
                public_id = ''
            return "Photo <%s:%s>" % (self.title, public_id)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE

    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def _str__(self):
        """Return the model as a string"""
        return self.status_text
