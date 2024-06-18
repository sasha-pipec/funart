from rest_framework import serializers

from models_app.models import UserColoring


class UserColoringSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='coloring.id')
    name = serializers.CharField(source='coloring.name')
    image = serializers.CharField(source='coloring.image')
    coloring_json = serializers.JSONField()

    class Meta:
        model = UserColoring
        fields = (
            'id',
            'name',
            'image',
            'coloring_json'
        )
