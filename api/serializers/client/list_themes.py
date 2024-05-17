from rest_framework import serializers
from models_app.models import Theme, LikeTheme
from api.serializers.category.list import CategoryListSerializer

# path('themes/client/<int:id>/', ClientThemeListGetView.as_view()),

class ClientThemeListSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    count_like = serializers.SerializerMethodField()

    def get_count_like(self, obj):
        return obj.likes.all().count()

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
            'count_like',
            'created_at',
            'updated_at',
            'rating'
        )
