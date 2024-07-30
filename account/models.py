from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from django.utils.translation import gettext_lazy as _
from .usermanager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(_('Email Address: '),unique=True,blank=False,null=False)
    is_verified=models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='Date Joined',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login',auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email if self.email else ""
    
    def token(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh': str(refresh),
            'access':str(refresh.access_token)
        }