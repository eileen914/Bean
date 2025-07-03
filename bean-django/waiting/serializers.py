from rest_framework import serializers
from .models import Waiting

class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waiting
        fields = '__all__'