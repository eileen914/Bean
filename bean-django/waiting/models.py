from django.db import models
from django.contrib.auth.models import User
from cafe.models import Cafe

# Create your models here.
class Waiting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    table_type_preference = models.CharField(max_length=20)
    notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} waiting @ {self.cafe.name}"
