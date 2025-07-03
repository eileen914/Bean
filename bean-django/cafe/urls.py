from django.urls import path
from .views import CafeUploadView, CafeListView, CafeDetailView, CafeImageUpdateView

app_name = 'cafe'

urlpatterns = [
    path("upload-cafes/", CafeUploadView.as_view(), name='upload_cafes'),
    path("update-images/", CafeImageUpdateView.as_view(), name='update_images'),
    path("", CafeListView.as_view()),
    path("<int:cafe_id>/", CafeDetailView.as_view()),
]