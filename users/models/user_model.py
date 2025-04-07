import secrets

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import slugify

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Must have email")
        if not password:
            raise ValueError("Insert password")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email=email, password=password, **extra_fields)

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, verbose_name="Username", null=False)
    email = models.EmailField(max_length=100, unique=True, verbose_name="Email", null=False)
    password = models.CharField(max_length=150, verbose_name="Password", null=False)
    age = models.IntegerField(null=False, default=18, blank=True, verbose_name="Age")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Phone")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active user?")
    is_staff = models.BooleanField(default=False, verbose_name="Allowed to be staff")
    is_superuser = models.BooleanField(default=False, verbose_name="Administrator?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last update')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name= "User"
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        if not self.slug:
            prov = secrets.token_urlsafe(16)
            while CustomUser.objects.filter(slug=prov).exists():
                prov = secrets.token_urlsafe(16)
            self.slug = prov
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.email}"


