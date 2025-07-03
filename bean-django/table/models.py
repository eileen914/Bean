from django.db import models
from cafe.models import Cafe

# Create your models here.
class Table(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='tables')
    type = models.CharField(max_length=20)  # ex: '1인석', '2인석', '단체석'
    has_power = models.BooleanField(default=False)
    near_window = models.BooleanField(default=False)
    is_occupied = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cafe.name} - {self.type}"
