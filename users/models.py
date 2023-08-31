from django.db import models
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            return ValueError('Email is required.')
        now = timezone.localtime()
        email = self.normalize_email(email)
        username = email.split('@')[0]
        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=155)
    username = models.CharField(max_length=255, null=False, blank=False)
    profile_img = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    # 이메일에서 username을 추출
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
