from django.urls import path
from .views import ReviewCrawlingView, ReviewListView

app_name = 'review'

urlpatterns = [
    path("crawl-reviews/", ReviewCrawlingView.as_view(), name="crawl_reviews"),
    path("", ReviewListView.as_view),
]