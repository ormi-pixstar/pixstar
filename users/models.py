from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):

    def _create_user (self, nickname, email,  password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError("User must have an E-mail")
        now = timezone.localtime()
        email = self.normalize_email(email)
        user = self.model(
            nickname = nickname,
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
    
    def create_user(self, nickname, email, password, **extra_fields):
        return self._create_user(nickname, email, password, False, False, **extra_fields)
    
    def create_staff(self, nickname, email, password, **extra_fields):
        return self._create_user(nickname, email, password, True, False, **extra_fields)
    
    def create_superuser(self, nickname, email, password, **extra_fields):
        return self._create_user(nickname, email, password, True, True, **extra_fields)
    
class User(AbstractBaseUser):
    nickname = models.CharField(unique=True, max_length=64)
    email = models.CharField(max_length=150, default='test@example.com')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'nickname'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.nickname
    

class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    # profileimg = models.ImageField()
