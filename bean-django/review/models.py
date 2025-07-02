from django.db import models
from django.contrib.auth.models import User
from cafe.models import Cafe
from tag.models import Tag

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    rating = models.FloatField()
    tags = models.ManyToManyField(Tag, blank=True, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} @ {self.cafe.name}"
