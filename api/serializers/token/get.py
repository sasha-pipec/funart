from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.authtoken.models import Token

from models_app.models import User


class GetTokenSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        obj_user = self.get_user(attrs['username'])
        self.check_password(obj_user, attrs['password'])
        attrs['token'] = self.get_token(obj_user)
        return attrs

    @staticmethod
    def get_token(obj):
        token_obj = Token.objects.filter(user=obj)
        if token_obj.exists():
            return token_obj.first().key
        return Token.objects.create(user=obj).key

    @staticmethod
    def check_password(obj, password):
        if not obj.check_password(password):
            raise Exception('Data is not valid')

    @staticmethod
    def get_user(username):
        return get_object_or_404(User, username=username)



class DeleteTokenSerialuzers(serializers.Serializer):

    def validate(self, attrs):
        obj_token = Token.objects.filter(user=self.context['user'])
        if not obj_token.exists():
            raise ValidationError('The user is not logged in')
        attrs['obj_token'] = obj_token.first()
        return attrs
