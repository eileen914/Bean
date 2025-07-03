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

class ReviewCrawlingView(APIView):
    def post(self, request):
        cafes = Cafe.objects.all()
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