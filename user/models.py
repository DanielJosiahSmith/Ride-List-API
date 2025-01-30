from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class CustomUser(AbstractBaseUser):
    """Custom User Model"""

    user_id = models.AutoField(primary_key=True)
    #user_id replaces username as primary key
    USERNAME_FIELD = "user_id"

    role = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user_id)