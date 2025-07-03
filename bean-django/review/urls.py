from django.urls import path
from .views import ReviewCrawlingView

app_name = 'review'

urlpatterns = [
    path("crawl-reviews/", ReviewCrawlingView.as_view(), name="crawl_reviews"),
]