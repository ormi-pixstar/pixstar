from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):

    def _create_user (self, username, email,  password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError("User must have an E-mail")
        now = timezone.localtime()
        email = self.normalize_email(email)
        user = self.model(
            username = username,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            is_active = True,
            last_login = now,
            date_joined = now,
            **extra_fields

        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)
    
    def create_staff(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, False, **extra_fields)
    
    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields)
    
class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(max_length=150, default='test@example.com')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
