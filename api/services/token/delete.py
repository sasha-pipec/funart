from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User


class TokenDeleteServices(ServiceWithResult):
    user = ModelField(User)

    def process(self):
        self.result = self.delete_token()
        return self

    def delete_token(self):
        obj_token_search = Token.objects.filter(user=self.cleaned_data['user'])
        if not obj_token_search.exists():
            raise ValidationError('The user is not logged in')
        obj_token_search.first().delete()
