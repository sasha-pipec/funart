from rest_framework import serializers
from models_app.models import Theme, LikeTheme
from api.serializers.category.list import CategoryListSerializer

#
class PersonalThemeListSerializer(serializers.ModelSerializer):
#     count_like = serializers.IntegerField()
#     is_liked = serializers.BooleanField()
#
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
