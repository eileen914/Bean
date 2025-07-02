from django.urls import path
from .views import CafeUploadView

app_name = 'cafe'

urlpatterns = [
    path("upload-cafes/", CafeUploadView.as_view(), name='upload_cafes'),
]
