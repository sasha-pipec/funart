from django import forms
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from service_objects.services import ServiceWithResult
from functools import lru_cache
from models_app.models import User


class TokenGetServices(ServiceWithResult):
    username = forms.CharField()
    password = forms.CharField()

    def process(self):
        self.password_verification()
        self.result = self.get_token()
        return self

    def get_token(self):
        token_obj = Token.objects.filter(user=self.get_user())
        if token_obj.exists():
            return token_obj.first()
        return Token.objects.create(user=self.get_user())

    def password_verification(self):
        obj_user = self.get_user()
        if not obj_user.check_password(self.cleaned_data['password']):
            raise Exception('Data is not valid')

    @lru_cache
    def get_user(self):
        return get_object_or_404(User, username=self.cleaned_data['username'])
