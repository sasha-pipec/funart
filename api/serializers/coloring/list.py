from rest_framework import serializers

from models_app.models import Coloring


class ColoringListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coloring
        fields = (
            'id',
            'name',
            'image',
            'type',
        )
