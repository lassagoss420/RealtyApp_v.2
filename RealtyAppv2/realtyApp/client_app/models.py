from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.conf import settings


#todo
#create custom user to allow email only registrayion
#copy client from base app, add images?
#add emails
#make views


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('You must use an email address!')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be staff.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be superuser.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Client(models.Model):
    class Meta:
        db_table = 'clients'
        get_latest_by = "created_at"

    CATEGORY = (
        ('Client', 'Client'),
        ('Agent', 'Agent'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profiles')
    category = models.CharField(max_length=255, null=True, choices=CATEGORY)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=126, null=True, blank=True)
    phone_no = models.CharField(max_length=10, null=True, blank=True, verbose_name='Phone No.')
    str_addr = models.CharField(max_length=255, null=True, blank=True, verbose_name='Street Address')
    listing = models.ForeignKey('base.Listing', on_delete=models.CASCADE, related_name='clients')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name