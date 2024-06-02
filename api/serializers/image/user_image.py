from rest_framework import serializers

from models_app.models import UserColoring


class UserColoringSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='coloring.name')
    base_image = serializers.CharField(source='coloring.image')
    image = serializers.CharField()

    class Meta:
        model = UserColoring
        fields = (
            'id',
            'name',
            'base_image',
            'image'
        )
