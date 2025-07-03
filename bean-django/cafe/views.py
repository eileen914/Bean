from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Cafe, CafeTagRating
from .serializers import CafeSerializer, CafeTagRatingSerializer, CafeTagRatingCreateSerializer
from drf_yasg.utils import swagger_auto_schema
from tag.models import Tag

from .utils.in_memory_faiss import search_similar_cafes
import traceback

import json
import os

class CafeListView(APIView):
    def get(self, request):
        try:
            posts =Cafe.objects.all()[:100]
            serializer = CafeSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
    
    def post(self, request):
        name = request.data.get("name")
        address = request.data.get("address")
        description = request.data.get("description")
        photo_urls = request.data.get("photo_urls")
        pos_connected = request.data.get("pos_connected")

        tag_contents = request.data.get("tags")
        keyword_contents = request.data.get("keywords")

        if not description:
            description = ""
        
        if not photo_urls:
            photo_urls = []
        
        if not pos_connected:
            pos_connected = False

        cafe = Cafe.objects.create(
                name=name,
                address=address,
                description=description,
                has_wifi=True,
                average_rating=0.0,
                photo_urls=photo_urls,
                pos_connected=pos_connected
            )

        if tag_contents is not None:
            for tag_content in tag_contents:
                tag = Tag.objects.create(content = tag_content)
                CafeTagRating.objects.create(cafe = cafe, tag = tag, rating = 0.0)

        if keyword_contents is not None:
            for keyword_content in keyword_contents:
                if not Tag.objects.filter(content = keyword_content).exists():
                    cafe.keywords.create(content = keyword_content)
                else:
                    cafe.keywords.add(Tag.objects.get(content = keyword_content))

        serializer = CafeSerializer(cafe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CafeDetailView(APIView):
    def get(self, request, cafe_id):
        try:
            cafe = Cafe.objects.get(id=cafe_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CafeSerializer(instance=cafe)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, cafe_id):
        try:
            cafe = Cafe.objects.get(id=cafe_id)
        except:
            return Response(
                {"detail": "Cafe Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        cafe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, cafe_id):
        try:
            cafe = Cafe.objects.get(id=cafe_id)
        except:
            return Response(
                {"detail": "Cafe not found."}, status=status.HTTP_404_NOT_FOUND
            )

        name = request.data.get("name")
        address = request.data.get("address")
        description = request.data.get("description")
        photo_urls = request.data.get("photo_urls")
        pos_connected = request.data.get("pos_connected")
        
        if name:
            cafe.name = name
        
        if address:
            cafe.address = address
        
        if description:
            cafe.description = description
        
        if photo_urls:
            cafe.photo_urls = photo_urls
        
        if pos_connected:
            cafe.pos_connected = pos_connected

        #tag_contents = request.data.get("tags") 일단 태그 데이터는 여기서 수정 X
        keyword_contents = request.data.get("keywords")

        
        if keyword_contents is not None:
            cafe.keywords.clear()
            for keyword_content in keyword_contents:
                if not Tag.objects.filter(content=keyword_content).exists():
                    cafe.keywords.create(content=keyword_content)
                else:
                    cafe.keywords.add(Tag.objects.get(content=keyword_content))

        cafe.save()
        serializer = CafeSerializer(instance=cafe)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CafeChatView(APIView):
    def post(self, request):
        try:
            question = request.data.get("question")
            if not question:
                return Response(
                    {"error": "question 필드를 전달해주세요."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # FAISS + RAG 검색
            cafes = search_similar_cafes(question, top_k=100)
        except Exception as e:
            traceback.print_exc()         # 터미널에 전체 에러 스택 출력
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # 직렬화
        # data = [
        #     {
        #         "id":          cafe.id,
        #         "name":        cafe.name,
        #         "address":     cafe.address,
        #         "description": cafe.description,
        #     }
        #     for cafe in cafes
        # ]
        # return Response({"results": data})

        #직렬화
        serializer = CafeSerializer(cafes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    
class CafeImageUpdateView(APIView):
    def put(self, request):
        base_path = "data/cafe_images/"
        idx = 0
        imageLen = 132

        cafes = Cafe.objects.all()
        for cafe in cafes:
            photo_urls = []
            for i in range(3):
                photoIndex = (idx%imageLen) + 1
                photo_url = f"{base_path}{photoIndex}.jpg"
                photo_urls.append(photo_url)
                idx += 1

            #print(f"Saving cafe {cafe.id} with images: {photo_urls}")
            cafe.photo_urls = photo_urls
            cafe.save()
            #print(f"Saved: {cafe.photo_urls}")
    
        return Response({"message": "Cafe images updated"}, status=status.HTTP_200_OK)

class CafeViewSet(viewsets.ModelViewSet):
    queryset = Cafe.objects.all().order_by('-created_at')
    serializer_class = CafeSerializer


class CafeTagRatingView(APIView):
    @swagger_auto_schema(
        operation_id='태그에 해당하는 카페와 별점 조회',
        operation_description='해당 태그에 대한 카페와 별점을 별점순으로 조회합니다.',
        responses={200: CafeTagRatingSerializer(many=True), 204: 'No Content'}
    )
    def get(self, request, tag_id):
        try:
            Tag.objects.get(id=tag_id)
        except:
            return Response({"detail": "Provided tag does not exist."}, status=status.HTTP_204_NO_CONTENT)
        
        cafeId = request.data.get("cafe_id")
        
        ratings = CafeTagRating.objects.filter(tag_id=tag_id).filter(cafe_id=cafeId).order_by('-rating')
        serializer = CafeTagRatingSerializer(instance=ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_id='카페와 태그에 따른 별점 생성',
        operation_description='카페와 태그에 따른 별점을 생성합니다.',
        request_body=CafeTagRatingSerializer,
        responses={201: CafeTagRatingSerializer}
    )
    def post(self, request):
        serializer = CafeTagRatingCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Check if Cafe and Tag exist
            cafe_id = serializer.validated_data['cafe'].id
            tag_id = serializer.validated_data['tag'].id
            if not Cafe.objects.filter(id=cafe_id).exists():
                return Response({"detail": "Cafe not found."}, status=status.HTTP_400_BAD_REQUEST)
            if not Tag.objects.filter(id=tag_id).exists():
                return Response({"detail": "Tag not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Save and respond
            rating_instance = serializer.save()
            full_serializer = CafeTagRatingSerializer(rating_instance)
            return Response(full_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CafeTagRatingDetailView(APIView):
    
    def get_object(self, rating_id):
        try:
            return CafeTagRating.objects.get(id=rating_id)
        except CafeTagRating.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_id='별점 수정',
        operation_description='특정 CafeTagRating의 별점을 수정합니다.',
        request_body=CafeTagRatingCreateSerializer,
        responses={200: CafeTagRatingSerializer, 404: 'Not Found'}
    )
    def put(self, request, rating_id):
        instance = self.get_object(rating_id)
        if not instance:
            return Response({"detail": "Rating not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CafeTagRatingCreateSerializer(instance, data=request.data)
        if serializer.is_valid():
            updated = serializer.save()
            return Response(CafeTagRatingSerializer(updated).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_id='별점 삭제',
        operation_description='특정 CafeTagRating을 삭제합니다.',
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def delete(self, request, rating_id):
        instance = self.get_object(rating_id)
        if not instance:
            return Response({"detail": "Rating not found."}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)