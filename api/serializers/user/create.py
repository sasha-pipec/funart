from rest_framework import serializers

from models_app.models import User


class CreateUserSerializzer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        self.check_user(attrs['username'])
        user = self.create_user(attrs)
        attrs['user'] = user

        return attrs

    def check_user(self, username):
        check_user = User.objects.filter(
            username=username
        )
        if check_user.exists():
            raise Exception('A user with that name already exists')

    def create_user(self, attrs):
        return User.objects.create_user(**attrs)


