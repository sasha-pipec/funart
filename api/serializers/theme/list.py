from rest_framework import serializers
from models_app.models import Theme
from api.serializers.category.list import CategoryListSerializer


class ThemeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theme
        fields = (
            'id',
            'name',
            'description',
            'image',
            'popular_image',
            'rating',
        )
