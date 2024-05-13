from rest_framework import serializers

from models_app.models import User


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username"
        )
