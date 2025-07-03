from django.urls import path
from .views import review_description, review_tag_rating, review_keyword

urlpatterns = [
    path('review_description/', review_description),
    path('review_tag_rating/', review_tag_rating),
    path('review_keyword/', review_keyword),
]