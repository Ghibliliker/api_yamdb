from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import User
from .confirmation_code import send_email_with_confirmation_code, create_code


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )

    def validate_username(self, value):

        if value is None:
            raise ValidationError("Field username is empty")

        return value

    def validate_email(self, value):

        if value is None:
            raise ValidationError("Field email is empty")

        return value


class UserSerializerForCode(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
        )
        model = User

    def validate_username(self, value):

        if value.lower() == "me":
            raise ValidationError("Wrong value for field username - me")

        return value

    """def create(self, validated_data):
        user = User.objects.create(**validated_data)
        code = create_code(user)
        send_email_with_confirmation_code(code, user.email)
        user.confirmation_code = code
        user.save()
        return user"""


class YamdbTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=30, required=True)

    def validate(self, data):
        user = get_object_or_404(
            User,
            username=data["username"]
            # confirmation_code=data["confirmation_code"]
        )
        if user.confirmation_code != data["confirmation_code"]:
            raise ValidationError("Wrong confirmation_code")
        return data
