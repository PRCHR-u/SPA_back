from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model.
    """
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, verbose_name='Phone', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Avatar', blank=True, null=True)
    country = models.CharField(max_length=100, verbose_name='Country', blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
