from rest_framework import serializers
from models_app.models import Theme, LikeTheme
from api.serializers.category.list import CategoryListSerializer


class ThemeListSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        user = self.context.get("user")
        if not user or user.is_anonymous:
            return False
        return LikeTheme.objects.filter(user=self.context['user'], theme=obj).exists()

    class Meta:
        model = Theme
        fields = (
            'id',
            'name',
            'description',
            'image',
            'is_liked',
            'created_at',
            'updated_at'
        )


class ThemeListPopularSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        user = self.context.get("user")
        if not user or user.is_anonymous:
            return False
        return LikeTheme.objects.filter(user=self.context['user'], theme=obj).exists()

    class Meta:
        model = Theme
        fields = (
            'id',
            'name',
            'popular_image',
            'is_liked',
            'created_at',
            'updated_at'
        )
