from rest_framework import serializers
from .models import SeatUsageLog
from tag.serializers import TagSerializer

class CafeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = SeatUsageLog
        fields = '__all__'