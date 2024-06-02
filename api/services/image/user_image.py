from functools import lru_cache

from django import forms
from rest_framework.exceptions import NotFound
from service_objects.services import ServiceWithResult

from models_app.models import UserColoring, Coloring


class UserColoringServices(ServiceWithResult):
    user_id = forms.IntegerField()
    coloring_id = forms.IntegerField()

    def process(self):
        self.result = self._get_image

        return self

    @property
    def _get_image(self):
        obj_image = UserColoring.objects.filter(coloring=self.search_coloring(),
                                                user_id=self.cleaned_data['user_id'])
        return obj_image.first()

    def search_coloring(self):
        obj_coloring = Coloring.objects.filter(id=self.cleaned_data['coloring_id'])
        if not obj_coloring.exists():
            raise NotFound('The coloring with such data was not found')
        return obj_coloring.first()
