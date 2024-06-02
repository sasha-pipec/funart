from rest_framework import serializers

from models_app.models import UserColoring


class UserColoringsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserColoring
        fields = (
            'id',
            'image'
        )
