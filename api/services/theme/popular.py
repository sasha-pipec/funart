from django.db.models import Count, Exists, OuterRef, Value
from django import forms
from service_objects.services import ServiceWithResult

from models_app.models import Theme, LikeTheme


class ThemePopularListService(ServiceWithResult):

    def process(self):
        self.result = self._popular_themes
        return self

    @property
    def _popular_themes(self):
        return Theme.objects.prefetch_related('likes').order_by("-rating")[:4]
