from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('owner', 'Dueño'),
        ('admin', 'Administrador'),
        ('seller', 'Vendedor'),
        ('customer', 'Cliente'),
    )

    user_type = models.CharField(
        choices=USER_TYPE_CHOICES, default='customer', max_length=20)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
