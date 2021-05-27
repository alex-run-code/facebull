from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import requests
from django.utils.timezone import datetime
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.


class CustomUserManager(BaseUserManager):
     """
     Custom user model manager where email is the unique identifiers
     for authentication instead of usernames.
     """
     def create_user(self, email, password, **extra_fields): # this
          """
          Create and save a User with the given email and password.
          """
          if not email:
               raise ValueError(_('The Email must be set'))
          email = self.normalize_email(email)
          user = self.model(email=email, **extra_fields)
          user.set_password(password)
          user.save()
          return user

     def create_superuser(self, email, password, **extra_fields):
          """
          Create and save a SuperUser with the given email and password.
          """
          extra_fields.setdefault('is_staff', True)
          extra_fields.setdefault('is_superuser', True)
          extra_fields.setdefault('is_active', True)

          if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
          if extra_fields.get('is_superuser') is not True:
               raise ValueError(_('Superuser must have is_superuser=True.'))
          return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
     """User model."""

     username = None
     email = models.EmailField(_('email address'), blank=True, unique=True)
     ip_joined = models.GenericIPAddressField(blank=True, null=True)
     holiday = models.BooleanField(default=False)

     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = []

     objects = CustomUserManager()

     def __str__(self):
        return self.email


class Post(models.Model):
     author = models.ForeignKey(User, on_delete=models.CASCADE)
     content = models.TextField(max_length=1000)

     def __str__(self):
          return f"Post from {str(self.author)} - id: {self.id}"


class Like(models.Model):
     post = models.ForeignKey(Post, on_delete=models.CASCADE)
     author = models.ForeignKey(User, on_delete=models.CASCADE)

     class Meta:
          unique_together = ('post', 'author',)


