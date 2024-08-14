from django import forms
from rest_framework import status
from service_objects.errors import ValidationError
from service_objects.services import ServiceWithResult

from models_app.models import Coloring, UserColoring

class UserColoringCreateService(ServiceWithResult):
    user_id = forms.IntegerField()
    coloring_id = forms.IntegerField()
    coloring_json = forms.JSONField()
    image = forms.ImageField()

    def process(self):
        self.create()
        return self

    def create(self):
        UserColoring.objects.create(
            user_id=self.cleaned_data['user_id'],
            coloring=self._coloring,
            image=self.cleaned_data['image'],
            coloring_json=self.cleaned_data["coloring_json"]
        )

    @property
    def _coloring(self):
        colorings = Coloring.objects.filter(id=self.cleaned_data['coloring_id'])
        if not colorings.exists():
            raise ValidationError(
                message='Раскраска не найдена.',
                response_status=status.HTTP_404_NOT_FOUND
            )
        return colorings.first()