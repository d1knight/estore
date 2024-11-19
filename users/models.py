from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    STATUS_CHOICES = [
        ("admin","Admin"),
        ("user","User")
    ]
    
    role = models.CharField(choices=STATUS_CHOICES, max_length=255)

    class Meta:
        db_table='users'


