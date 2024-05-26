from django import forms
from django.db.models import Count

from service_objects.services import ServiceWithResult

from models_app.models import Coloring, Theme


class ColoringCreateServices(ServiceWithResult):
    id = forms.IntegerField()
    name = forms.CharField()
    image = forms.ImageField()

    def process(self):
        self.result = self._create_coloring()
        return self

    def _create_coloring(self):
        coloring = Coloring.objects.create(
            name=self.cleaned_data['name'],
            image=self.cleaned_data['image'],
            theme=self._get_theme
        )
        return coloring

    @property
    def _get_theme(self):
        return Theme.objects.get(id=self.cleaned_data['id'])
