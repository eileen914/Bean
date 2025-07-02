from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Cafe
from .serializers import CafeSerializer

class CafeViewSet(viewsets.ModelViewSet):
    queryset = Cafe.objects.all().order_by('-created_at')
    serializer_class = CafeSerializer
