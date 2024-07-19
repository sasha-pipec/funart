from django import forms
from service_objects.services import ServiceWithResult

from models_app.models import Banner


class BannerCreateService(ServiceWithResult):
    heading = forms.CharField()
    description = forms.CharField()
    image = forms.ImageField()

    def process(self):
        self.result = self._create_banner()
        return self

    def _create_banner(self):
        banner = Banner.objects.create(
            heading=self.cleaned_data['heading'],
            description=self.cleaned_data['description'],
            image=self.cleaned_data['image']
        )
        return banner
