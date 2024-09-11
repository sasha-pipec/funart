from functools import lru_cache

from django import forms
from rest_framework import status
from service_objects.errors import ValidationError
from service_objects.services import ServiceWithResult

from models_app.models import UserColoring
from utils.manager_helpers import get_or_none


class UserColoringDeleteService(ServiceWithResult):
    id = forms.IntegerField()

    custom_validations = ['_user_coloring_presence']

    def process(self):
        self.run_custom_validations()
        self._delete_user_coloring()
        return self

    def _delete_user_coloring(self):
        self._user_coloring.delete()

    def _user_coloring_presence(self):
        if not self._user_coloring:
            raise ValidationError(
                message='Раскраска не найдена.',
                response_status=status.HTTP_404_NOT_FOUND
            )

    @property
    @lru_cache()
    def _user_coloring(self):
        return get_or_none(UserColoring, id=self.cleaned_data['id'])
