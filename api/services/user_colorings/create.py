from django import forms
from rest_framework import status
from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import Coloring, UserColoring, User
from utils.manager_helpers import get_or_none


class UserColoringCreateService(ServiceWithResult):
    user = ModelField(User)
    coloring_id = forms.IntegerField()
    coloring_json = forms.JSONField()
    image = forms.ImageField()

    custom_validations = ['_coloring_presence']

    def process(self):
        self.run_custom_validations()
        self._create_coloring()
        return self

    def _create_coloring(self):
        return UserColoring.objects.create(**self.cleaned_data)

    @property
    def _coloring(self):
        return get_or_none(Coloring, id=self.cleaned_data['coloring_id'])

    def _coloring_presence(self):
        if not self._coloring:
            raise ValidationError(
                message='Раскраска не найдена.',
                response_status=status.HTTP_404_NOT_FOUND
            )
