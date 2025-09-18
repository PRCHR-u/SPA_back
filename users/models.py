from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model that uses 'username' for login but requires a unique email.
    This inherits all fields from AbstractUser (including username, password, email, etc.)
    """
    # By default, AbstractUser has USERNAME_FIELD = 'username'. We will stick to that.
    # We are overriding the email field to make it required and unique.
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        help_text='Required. Enter a valid email address.'
    )

    # These fields are optional additions to the user model
    phone = models.CharField(max_length=35, verbose_name='Phone', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Avatar', blank=True, null=True)
    country = models.CharField(max_length=100, verbose_name='Country', blank=True, null=True)

    # REQUIRED_FIELDS are fields prompted for when creating a superuser.
    # 'username' and 'password' are required by default.
    # We are adding 'email' to this list.
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
