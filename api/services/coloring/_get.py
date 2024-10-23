from functools import lru_cache

from django import forms
from rest_framework.exceptions import NotFound
from service_objects.services import ServiceWithResult

from models_app.models import Coloring
from utils.get_object_or_none import get_object_or_none


class ColoringGetService(ServiceWithResult):
    coloring_id = forms.IntegerField()

    custom_validations = ["_coloring_presence"]

    def process(self):
        pass

    @lru_cache
    @property
    def _coloring(self):
        return get_object_or_none(Coloring, self.cleaned_data["coloring_id"])

    def _coloring_presence(self):
        if not self._coloring:
            raise NotFound("Coloring not found.")
