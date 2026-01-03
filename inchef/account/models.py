from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('chef', 'Chef'),
        ('client', 'Client'),
    )
    phone_number = models.CharField(max_length=13, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile/avatar', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username