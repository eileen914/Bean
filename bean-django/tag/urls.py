from django.urls import path
from .views import TagListView, CafeTagRatingView, CafeTagRatingDetailView

app_name = 'tag'

urlpatterns = [
    path("", TagListView.as_view),
]
