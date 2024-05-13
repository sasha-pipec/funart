from django.db.models import Count
from service_objects.services import ServiceWithResult

from models_app.models import Theme


class ThemePopularListServices(ServiceWithResult):

    def process(self):
        self.result = self._popular_themes
        return self

    @property
    def _popular_themes(self):
        return (
            Theme.objects
            .prefetch_related('likes')
            .annotate(likes_count=Count('likes'))
            .all()
            .order_by("-rating")
        )[:4]
