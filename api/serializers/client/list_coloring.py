from rest_framework import serializers
from models_app.models import Theme, LikeTheme, LikeColoring, Coloring
from api.serializers.category.list import CategoryListSerializer


class ClientColoringListSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    count_like = serializers.SerializerMethodField()
    theme = serializers.CharField(source='theme.name')

    def get_count_like(self, obj):
        return obj.coloring_likes.all().count()

    def get_is_liked(self, obj):
        user = self.context.get("user")
        if not user or user.is_anonymous:
            return False
        return LikeColoring.objects.filter(user=self.context['user'], coloring=obj).exists()

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
