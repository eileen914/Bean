from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Cafe
from .serializers import CafeSerializer

import json
import os

class CafeUploadView(APIView):
    def post(self, request):
        file_path = "data/cafe_opened_data.json"  # 로컬 경로 지정 (프로젝트 기준 상대경로 또는 절대경로 사용)

        if not os.path.exists(file_path):
            return Response({"detail": f"File not found: {file_path}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return Response({"detail": "Invalid JSON format."}, status=status.HTTP_400_BAD_REQUEST)

        created_cafes = []

        for item in data:
            name = item.get('bplcnm')
            address = item.get('rdnwhladdr')
            if not name or not address:
                continue  # 필수 필드 없으면 무시

            cafe = Cafe.objects.create(
                name=name,
                address=address,
                description="",
                has_wifi=True,
                average_rating=0.0,
                photo_urls=[],
                pos_connected=False
            )
            created_cafes.append(cafe)

        serializer = CafeSerializer(created_cafes, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CafeViewSet(viewsets.ModelViewSet):
    queryset = Cafe.objects.all().order_by('-created_at')
    serializer_class = CafeSerializer