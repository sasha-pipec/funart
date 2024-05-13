from rest_framework import status
from rest_framework.authtoken.models import Token
from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User


class TokenDeleteServices(ServiceWithResult):
    user = ModelField(User)

    def process(self):
        self.delete_token()
        return self

    def delete_token(self):
        self.cleaned_data['user'].auth_token.delete()
