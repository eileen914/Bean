from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserProfile

class UserIdUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]


class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = "__all__"