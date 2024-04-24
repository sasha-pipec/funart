from django import forms
from rest_framework.authtoken.models import Token
from service_objects.services import ServiceWithResult

from models_app.models import User


class UserCreateServices(ServiceWithResult):
    username = forms.CharField()
    password = forms.CharField()

    def process(self):
        self.check_user()
        self.create_user_and_token()
        return self

    def check_user(self):
        check_user = User.objects.filter(
            username=self.cleaned_data['username']
        )
        if check_user.exists():
            raise Exception('A user with that name already exists')

    def create_user_and_token(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        Token.objects.create(user=user)
