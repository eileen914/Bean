from rest_framework import serializers

class SignUpRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    username = serializers.CharField()
    phone = serializers.CharField()
    birth = serializers.DateField()


class SignInRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()