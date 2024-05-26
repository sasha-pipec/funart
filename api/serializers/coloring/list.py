from rest_framework import serializers

from models_app.models import Coloring


class ColoringListSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField()
    likes_count = serializers.IntegerField()

    class Meta:
        model = Coloring
        fields = (
            'id',
            'name',
            'image',
            'is_liked',
            'likes_count',
            'theme'
        )
