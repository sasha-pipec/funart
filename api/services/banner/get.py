from django import forms
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult
from models_app.models import Banner


class BannerDetailService(ServiceWithResult):
    id = forms.IntegerField()

    def process(self):
        self.result = self._get_banner_object
        return self

    @property
    def _get_banner_object(self):
        banner = Banner.objects.filter(id=self.cleaned_data['id'])
        if not banner.exists():
            raise NotFound(message="Баннер не найден.", response_status=404)
        return banner.first()
