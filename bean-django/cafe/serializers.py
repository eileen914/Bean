from rest_framework import serializers
from .models import Cafe, CafeTagRating
from tag.serializers import TagSerializer

class CafeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Cafe
        fields = '__all__'

class CafeTagRatingSerializer(serializers.ModelSerializer):
    cafes = CafeSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = CafeTagRating
        fields = '__all__'