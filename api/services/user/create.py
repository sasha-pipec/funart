from django import forms
from rest_framework import status
from service_objects.errors import ValidationError
from service_objects.services import ServiceWithResult

from models_app.models import User


class UserCreateService(ServiceWithResult):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField()

    def process(self):
        self.user_presence()
        self.result = self.create_user()
        return self

    def user_presence(self):
        users = User.objects.filter(email=self.cleaned_data['email'])
        if users.exists():
            raise ValidationError(
                message='Пользователь с таким email уже существует.',
                response_status=status.HTTP_400_BAD_REQUEST
            )

    def create_user(self):
        return User.objects.create_user(
            email=self.cleaned_data['email'],
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
