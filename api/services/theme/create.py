from django import forms
from service_objects.services import ServiceWithResult

from models_app.models import Theme


class ThemeCreateService(ServiceWithResult):
    name = forms.CharField()
    description = forms.CharField()
    image = forms.ImageField()

    def process(self):
        self.result = self._create_theme()
        return self

    def _create_theme(self):
        theme = Theme.objects.create(
            name=self.cleaned_data['name'],
            description=self.cleaned_data['description'],
            image=self.cleaned_data['image'],
        )
        return theme
