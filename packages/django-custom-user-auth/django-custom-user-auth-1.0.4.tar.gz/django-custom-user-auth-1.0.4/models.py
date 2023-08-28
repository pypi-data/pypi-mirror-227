from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from .mixins import CustomPermissionsMixin
import uuid

# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    
    A custom version of the BaseUserManager model that implements 
    the creation of users and superusers. 

    """

    use_in_migrations = True

    def create_user(self, username: str, password: str, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not password:
            raise ValueError('The given password must be set')
    
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, username: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """

    Base user model that contains the common user credentials. This model also allows
    composition wherein other models would have a 'has-a' relationship. Examples are: 
    doctor model or patient model. To implement composition from this, just import the 
    model e.g. 'from user.models import User' (if in another app) then to implement 
    composition:

    class Patient(models.Model):
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
        ....
     
    """

    username_validator = UnicodeUsernameValidator()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255, unique=True, validators=[username_validator])
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    groups = CustomPermissionsMixin.groups
    user_permissions = CustomPermissionsMixin.user_permissions

    def set_password(self, raw_password: str):
        super().set_password(raw_password)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)