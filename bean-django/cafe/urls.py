from django.urls import path
from .views import CafeUploadView, CafeListView, CafeDetailView, CafeImageUpdateView, CafeChatView, CafeTagRatingView, CafeTagRatingDetailView

app_name = 'cafe'

urlpatterns = [
    path("upload-cafes/", CafeUploadView.as_view(), name='upload_cafes'),
    path("update-images/", CafeImageUpdateView.as_view(), name='update_images'),
    path("", CafeListView.as_view()),
    path("<int:cafe_id>/", CafeDetailView.as_view()),
    path("chat/", CafeChatView.as_view(), name='chat'),
    path("tagrating/<int:tag_id>/", CafeTagRatingView.as_view),
    path("tagrating/detail/<int:rating_id>/", CafeTagRatingDetailView.as_view),
]