from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username, email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True, default="")
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELD = "username"

    def __str__(self):
        return str(self.username)


class Book(models.Model):
    title = models.CharField(max_length=100, default="")
    author = models.CharField(max_length=100, default="")
    isbn = models.CharField(max_length=100, unique=True)
    publication_year = models.CharField(max_length=5, default="")
    genre = models.CharField(max_length=30, default="")
    is_available = models.BooleanField(default=True)


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    return_date = models.DateField(default=datetime.date.today, null=True)
