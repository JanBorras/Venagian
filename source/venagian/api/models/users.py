import logging

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

LANGUAGES = (
    ("Spanish", "Spanish"),
    ("English", "English"),
    ("Catalan", "Catalan"),
)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users require an email field")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("username", email)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("username", email)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    """
    Note that AbstractUser already has:
        * username
        * first_name
        * last_name
        * email

    More:
    https://github.com/django/django/blob/main/django/contrib/auth/models.py#L334
    """

    class Meta:
        db_table = "api_user"
        verbose_name = "User"
        ordering = ["-id"]

    objects = UserManager()
    email = models.EmailField(unique=True)
    language = models.CharField(
        choices=LANGUAGES, default="Spanish", max_length=100
    )
    phone = models.CharField(max_length=100, blank=True, default="")
    address = models.CharField(max_length=100, blank=True, default="")
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, default="")
    account_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        self.username = self.email
        super(User, self).save(*args, **kwargs)