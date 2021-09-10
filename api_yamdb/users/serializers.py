from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
# from rest_framework.relations import StringRelatedField

from .models import User
from .confirmation_code import send_email_with_confirmation_code, create_code


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserSerializerForCode(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id", "username",
            "first_name", "last_name",
            "email", "bio", "role"
        )
        model = User

    def validate_username(self, value):

        if value.lower() == "me":
            raise ValidationError("Wrong value for field username - me")

        return value

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        code = create_code(user)
        send_email_with_confirmation_code(code, user.email)
        return user


class YamdbTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=30, required=True)

    def validate(self, data):
        get_object_or_404(User, username=data["username"])
        return data
