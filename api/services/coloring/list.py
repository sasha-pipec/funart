from django import forms
from django.db.models import Count, Exists, OuterRef, Value
from rest_framework import status
from service_objects.errors import ValidationError
from service_objects.services import ServiceWithResult
from functools import lru_cache

from models_app.models import Coloring, Theme, LikeTheme, LikeColoring
from utils.paginator import paginated_queryset

ORDER_BY = {
    ('updated_at', True): 'updated_at',
    ('updated_at', False): '-updated_at',
    ('likes_count', True): 'likes_count',
    ('likes_count', False): '-likes_count',
}


class ColoringListService(ServiceWithResult):
    page = forms.IntegerField(required=False, min_value=1)
    per_page = forms.IntegerField(required=False, min_value=1)
    order_by = forms.CharField(required=False)
    id = forms.IntegerField()
    user_id = forms.IntegerField(required=False)

    def process(self):
        self._paginated_colorings()
        self._update_rating()
        return self

    def _paginated_colorings(self):
        self.result = paginated_queryset(
            queryset=self._colorings,
            page=self.cleaned_data.get("page"),
            per_page=self.cleaned_data.get("per_page")
        )
        self.result["theme"] = self._theme_presence

    @property
    @lru_cache
    def _theme_presence(self):
        themes = Theme.objects.prefetch_related('likes').filter(id=self.cleaned_data['id'])
        if not themes.exists():
            raise ValidationError(
                message='Тематика не найдена.',
                response_status=status.HTTP_404_NOT_FOUND
            )
        return themes.first()

    @property
    def _colorings(self):
        return Coloring.objects.filter(theme=self._theme_presence).order_by(
            ORDER_BY.get((self.cleaned_data['order_by'], False), '-id')
        )



    @lru_cache
    def _update_rating(self):
        theme = self._theme_presence
        theme.rating += 1
        theme.save()
