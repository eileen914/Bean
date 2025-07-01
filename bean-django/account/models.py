from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_preferences = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"id={self.id}, user_id={self.user.id}"