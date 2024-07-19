from service_objects.services import ServiceWithResult

from models_app.models import Banner
from utils.paginator import paginated_queryset


class BannerListService(ServiceWithResult):
    def process(self):
        self._paginated_themes()
        return self

    @property
    def _banners(self):
        return Banner.objects.all().order_by("heading")

    def _paginated_themes(self):
        self.result = paginated_queryset(
            queryset=self._banners,
            page=self.cleaned_data.get("page"),
            per_page=self.cleaned_data.get("per_page")
        )
