from rest_framework import serializers
from models_app.models import Theme, LikeTheme


class ThemeListSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField()
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return LikeTheme.objects.filter(theme=obj).count()

    class Meta:
        model = Theme
        fields = (
            'id',
            'name',
            'description',
            'image',
            'is_liked',
            'likes_count',
            'created_at',
            'updated_at',
            'rating'
        )


class ThemeListPopularSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField()
    likes_count = serializers.IntegerField()

    def get_likes_count(self, obj):
        return LikeTheme.objects.filter(theme=obj).count()

    class Meta:
        model = Theme
        fields = (
            'id',
            'name',
            'popular_image',
            'is_liked',
            'likes_count',
            'created_at',
            'updated_at',
            'rating'
        )
