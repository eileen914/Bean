from django.db import models
from cafe.models import Cafe
from table.models import Table

# Create your models here.
class SeatUsageLog(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    occupied = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cafe.name} - {self.table.id} - {'사용중' if self.occupied else '비어있음'}"
