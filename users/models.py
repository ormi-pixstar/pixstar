from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, name, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('User must have an email')
        now = timezone.localtime()
        email = self.normalize_email(email)
        user = self.model(
            name = name,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            date_joined = now,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, name, email, password, **extra_fields):
        return self._create_user(name, email, password, False, False, **extra_fields)
    
    def create_superuser(self, name, email, password, **extra_fields):
        return self._create_user(name, email, password, True, True, **extra_fields)
    
class User(AbstractBaseUser):
    name = models.CharField(unique=True, max_length=64)
    email = models.EmailField(max_length=155)
    profileimg = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.name
    
# class Profile(models.Model):
#     user = models.OneToOneField('User', on_delete=models.CASCADE)
#     # profileimg = models.ImageField(upload_to='media/def_img.jpg')
#     profileimg = models.CharField(null=True, default='이미지가 등록되지 않았습니다.', max_length=100)
#     create_at = models.DateTimeField(auto_now_add=True)
