from django.db import models
from django.contrib.auth.models import User
from cafe.models import Cafe
from table.models import Table

# Create your models here.
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('reserved', '예약중'),
        ('cancelled', '취소됨'),
        ('completed', '완료됨')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reserved')

    def __str__(self):
        return f"{self.user.username} @ {self.cafe.name} ({self.reservation_time})"
