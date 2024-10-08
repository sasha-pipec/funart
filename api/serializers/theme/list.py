from django.db.models import Exists
from rest_framework import serializers

from models_app.models import Theme, LikeTheme

#  Todo ______themes/<int:id>/colorings/___________________________________________________

class ThemeListSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        return True if LikeTheme.objects.filter(
            theme_id=obj.id, user_id=self.context['user_id']
        ).exists() else False

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
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        return True if LikeTheme.objects.filter(
            theme_id=obj.id, user_id=self.context['user_id']
        ).exists() else False

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
