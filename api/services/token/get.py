from django import forms
from rest_framework import status
from rest_framework.authtoken.models import Token
from service_objects.errors import ValidationError
from service_objects.services import ServiceWithResult
from functools import lru_cache
from models_app.models import User


class TokenGetOrCreateServices(ServiceWithResult):
    email = forms.EmailField()
    password = forms.CharField()

    def process(self):
        self.check_password()
        self.result = self._user_with_token
        return self

    def check_password(self):
        user = self._user_with_token
        if not user.check_password(self.cleaned_data['password']):
            raise ValidationError(
                message='Invalid password',
                response_status=status.HTTP_400_BAD_REQUEST
            )

    @property
    @lru_cache
    def _user_with_token(self):
        users = User.objects.filter(email=self.cleaned_data['email'])
        if not users.exists():
            raise ValidationError(
                message='User not found',
                response_status=status.HTTP_404_NOT_FOUND
            )
        user = users.first()
        if not hasattr(user, 'auth_token'):
            Token.objects.create(user=user)
        return user
