from rest_framework import serializers

from models_app.models import UserColoring


class UserColoringSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='coloring.id')
    name = serializers.CharField(source='coloring.name')
    image = serializers.SerializerMethodField()
    coloring_json = serializers.JSONField()

    def get_image(self, obj):
        return obj.coloring.image.url

    class Meta:
        model = UserColoring
        fields = (
            'id',
            'name',
            'image',
            'coloring_json'
        )
