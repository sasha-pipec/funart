from functools import lru_cache

from django import forms
from django.db.models import Count, OuterRef, Exists, Value
from service_objects.services import ServiceWithResult

from models_app.models import Coloring, LikeColoring, Theme, LikeTheme


class ColoringGetService(ServiceWithResult):
    id = forms.IntegerField()
    user_id = forms.IntegerField(required=False)

    def process(self):
        self.result = {
            "coloring": self._get_coloring,
            "themes": self._see_more_themes,
        }
        return self

    @property
    @lru_cache
    def _get_coloring(self):
        return Coloring.objects.select_related("theme").annotate(
            likes_count=Count('coloring_likes'),
            is_liked=(
                Exists(LikeColoring.objects.filter(
                    coloring=OuterRef('id'),
                    user_id=self.cleaned_data['user_id']
                ))
                if self.cleaned_data['user_id']
                else Value(False)
            )
        ).get(id=self.cleaned_data['id'])

    @property
    def _see_more_themes(self):
        return Theme.objects.prefetch_related('likes').annotate(
            likes_count=Count('likes'),
            is_liked=(
                Exists(LikeTheme.objects.filter(
                    theme=OuterRef('id'), user_id=self.cleaned_data['user_id']
                ))
                if self.cleaned_data['user_id']
                else Value(False)
            )
        ).filter(
            category__in=self._get_coloring.theme.category.values_list("id", flat=True)
        ).order_by('-updated_at')[:6]
