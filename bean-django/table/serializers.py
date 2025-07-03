from rest_framework import serializers
from .models import Table

class CafeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Table
        fields = '__all__'