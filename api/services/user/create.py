from django import forms
from rest_framework import status
from service_objects.errors import ValidationError
from service_objects.services import ServiceWithResult

from models_app.models import User


class UserCreateServices(ServiceWithResult):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField()

    def process(self):
        self.check_user()
        self.result = self.create_user()
        return self

    def check_user(self):
        user = User.objects.filter(email=self.cleaned_data['email'])
        if user.exists():
            raise ValidationError(
                message='A user with that email already exists',
                response_status=status.HTTP_400_BAD_REQUEST
            )

    def create_user(self):
        return User.objects.create_user(
            email=self.cleaned_data['email'],
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
