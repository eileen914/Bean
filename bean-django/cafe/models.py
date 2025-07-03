from django.db import models
from tag.models import Tag

# Create your models here.
class Cafe(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    average_rating = models.FloatField(default=0.0)
    photo_urls = models.JSONField(default=list, blank=True)  # list
    pos_connected = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, through='CafeTagRating', related_name='cafes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.address})"
    
class CafeTagRating(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('cafe', 'tag')
