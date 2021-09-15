from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import User
from .confirmation_code import create_code, send_email_with_confirmation_code


class UsersSerializer(serializers.ModelSerializer):
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


class MeSerializer(serializers.ModelSerializer):
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

    def validate(self, data):
        user = self.context['request'].user
        if user.is_user and ('role' in data):
            data.pop('role')
        return data


class UserSerializerForCode(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            'username',
            'email',
        )
        model = User

    def validate_username(self, value):

        if value.lower() == 'me':
            raise ValidationError('Wrong value for field username - me')

        return value

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        code = create_code(user)
        send_email_with_confirmation_code(code, validated_data['email'])
        user.confirmation_code = code
        return user


class YamdbTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=30, required=True)

    def validate(self, data):
        user = get_object_or_404(
            User,
            username=data['username']
        )
        if user.confirmation_code != data['confirmation_code']:
            raise ValidationError('Wrong confirmation_code')
        return data
