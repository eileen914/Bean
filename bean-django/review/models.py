from django.db import models
from django.contrib.auth.models import User
from cafe.models import Cafe

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    rating = models.FloatField()
    tags = models.JSONField(default=list, blank=True)  # ex: ['조용함', '콘센트']
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} @ {self.cafe.name}"
