from django.urls import path
from .views import TagListView

app_name = 'tag'

urlpatterns = [
    path("", TagListView.as_view),
]
