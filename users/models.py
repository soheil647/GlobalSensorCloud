from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    PERMISSION_CHOICES = [
        ('admin', 'admin'),
        ('organization', 'organization'),
        ('driver', 'driver'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    permission = models.CharField(max_length=20, choices=PERMISSION_CHOICES, default='driver')
    organization = models.CharField(max_length=100)

    def __str__(self):
        return f"User {self.user.username} with Permission {self.permission} from {self.organization}"