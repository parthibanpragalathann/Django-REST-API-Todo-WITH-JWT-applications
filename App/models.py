from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    name = models.CharField(max_length=110, blank=True, default="")
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=110)
    age = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

def profile_picture(instance, filename):
    #Function for save profile images.
    return '/'.join(['profile', str(instance.id), filename])

class UserProfile(models.Model):
    profile= models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to=profile_picture, blank=True, null=True)       #profile picture

class Task(models.Model):
    user = models.ForeignKey(CustomUser, related_name='todo_user', on_delete=models.PROTECT, null=True)
    title = models.CharField(max_length=110, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    completed = models.BooleanField(default=False)
