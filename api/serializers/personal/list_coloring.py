from rest_framework import serializers

from models_app.models import LikeColoring, Coloring


class ClientColoringListSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField()
    count_like = serializers.IntegerField()
    theme = serializers.CharField(source='theme.name')

    class Meta:
        model = Coloring
        fields = (
            'id',
            'name',
            'image',
            'is_liked',
            'count_like',
            'created_at',
            'updated_at',
            'theme'
        )
