from rest_framework import serializers

from .models import Title, Genre, Category, GenreTitle


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = serializers.SlugRelatedField(
        read_only=True, slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Title