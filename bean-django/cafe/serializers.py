from rest_framework import serializers
from .models import Cafe
from tag.serializers import TagSerializer

class CafeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Cafe
        fields = '__all__'
