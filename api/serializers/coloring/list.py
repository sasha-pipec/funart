from rest_framework import serializers

from api.serializers.theme.list import ThemeListSerializer
from models_app.models import Coloring, LikeColoring

#  Todo ______themes/<int:id>/colorings/___________________________________________________

class ColoringListSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    next = serializers.IntegerField(default=None)
    previous = serializers.IntegerField(default=None)

    def get_likes_count(self, obj):
        return obj.coloring_likes.count()

    def get_is_liked(self, obj):
        return True if LikeColoring.objects.filter(
            coloring_id=obj.id, user_id=self.context['user_id']
        ).exists() else False

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
