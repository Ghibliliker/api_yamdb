from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from .models import User
from .confirmation_code import send_email_with_confirmation_code


class UserSerializer(serializers.ModelSerializer):
    username = StringRelatedField(many=False)

    email = StringRelatedField(many=False)

    class Meta:
        fields = ("id", "username", "email", "bio", "role")
        model = User


class YamdbTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email

        return token
