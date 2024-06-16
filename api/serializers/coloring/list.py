from rest_framework import serializers

from api.serializers.theme.list import ThemeListSerializer
from models_app.models import Coloring


class ColoringListSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField()
    likes_count = serializers.IntegerField()
    next = serializers.IntegerField()
    previous = serializers.IntegerField()

    class Meta:
        model = Coloring
        fields = (
            'id',
            'name',
            'image',
            'is_liked',
            'likes_count',
            'theme',
            'next',
            'previous'
        )


class ColoringDetailSerializer(serializers.Serializer):
    coloring = ColoringListSerializer()
    themes = ThemeListSerializer(many=True)

