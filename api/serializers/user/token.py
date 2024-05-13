from rest_framework import serializers

from models_app.models import User


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        return obj.auth_token.key

    class Meta:
        model = User
        fields = (
            "token",
        )
