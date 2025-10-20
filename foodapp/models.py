from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=20)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
