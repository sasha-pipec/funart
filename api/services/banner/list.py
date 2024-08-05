from service_objects.services import ServiceWithResult

from models_app.models import Banner


class BannerListService(ServiceWithResult):
    def process(self):
        self.result = self._banners
        return self

    @property
    def _banners(self):
        return Banner.objects.all()
