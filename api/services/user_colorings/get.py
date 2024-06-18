from django import forms
from rest_framework import status
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from models_app.models import UserColoring, Coloring


class UserColoringGetService(ServiceWithResult):
    user_id = forms.IntegerField()
    user_coloring_id = forms.IntegerField()

    def process(self):
        self.result = self._user_coloring
        return self

    @property
    def _user_coloring(self):
        user_colorings = UserColoring.objects.filter(
            id=self.cleaned_data['user_coloring_id'],
            user_id=self.cleaned_data['user_id']
        )
        if not user_colorings.exists():
            raise NotFound(
                message='Раскрашенная hаскраска не найдена.',
                response_status=status.HTTP_404_NOT_FOUND
            )
        return user_colorings.first()
