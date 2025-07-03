from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cafe.models import Cafe
from review.models import Review
from review.serializers import ReviewSerializer
from django.contrib.auth.models import User
from utils.crawling import get_reviews_by_cafe_name
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ReviewCrawlingView(APIView):
    def post(self, request):
        #cafes = Cafe.objects.all()
        cafes = Cafe.objects.filter(address__contains="관악구")
        total_created = 0
        results = []

        for cafe in cafes:
            try:
                reviews = get_reviews_by_cafe_name(cafe.name)
                created_reviews = []
                for review_text in reviews:
                    review = Review.objects.create(
                        user= None,
                        cafe=cafe,
                        rating=0.0,
                        content=review_text
                    )
                    created_reviews.append(review)
                    total_created += 1
                results.append({
                    "cafe": cafe.name,
                    "review_count": len(created_reviews)
                })
            except Exception as e:
                results.append({
                    "cafe": cafe.name,
                    "error": str(e)
                })

        return Response({
            "total_reviews_created": total_created,
            "result": results
        }, status=status.HTTP_201_CREATED)

class ReviewListView(APIView):
    @swagger_auto_schema(
        operation_id='리뷰 목록 조회',
        operation_description='리뷰 목록을 조회합니다.',
        responses={200: ReviewSerializer(many=True)}
    )
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(instance=reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReviewDetailView(APIView):
    @swagger_auto_schema(
        operation_id='카페별 리뷰 목록 조회',
        operation_description='카페별 리뷰 목록을 조회합니다.',
        manual_parameters=[
            openapi.Parameter(
                'cafe_id', openapi.IN_PATH, 
                description="조회할 카페의 ID", 
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: ReviewSerializer(many=True)}
    )
    def get(self, request, cafe_id):
        try:
            Cafe.objects.get(pk=cafe_id)
        except Cafe.DoesNotExist:
            return Response({'detail': 'Cafe not found'}, status=status.HTTP_404_NOT_FOUND)
        reviews = Review.objects.filter(cafe_id=cafe_id)
        serializer = ReviewSerializer(instance=reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
