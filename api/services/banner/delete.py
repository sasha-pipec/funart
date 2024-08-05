import os

from django import forms
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from conf.settings.django import BASE_DIR
from models_app.models import Banner


class BannerDeleteService(ServiceWithResult):
    id = forms.IntegerField()


    def process(self):
        banner = self.get_banner_object()
        self.delete_banner(banner)
        return self


    def delete_banner(self, banner):
        os.remove(os.path.join(BASE_DIR, banner.image.url[1:]))
        banner.delete()
        return self

    def get_banner_object(self):
        banner = Banner.objects.filter(id=self.cleaned_data['id'])
        if not banner.exists():
            raise NotFound(message="Баннер не найден.", response_status=404)
        return banner.first()

