import json

from django import forms
from django.core.paginator import Paginator
from django.db.models import Count, Exists, OuterRef, Value
from rest_framework import status
from service_objects.errors import ValidationError
from service_objects.services import ServiceWithResult
from functools import lru_cache

from conf.settings.rest_framework import REST_FRAMEWORK
from models_app.models import Coloring, Theme, User, LikeTheme, LikeColoring


class ColoringListService(ServiceWithResult):
    page = forms.IntegerField(required=False, min_value=1)
    per_page = forms.IntegerField(required=False, min_value=1)
    id = forms.IntegerField()
    user_id = forms.IntegerField(required=False)

    def process(self):
        self._paginated_colorings()
        self._update_rating()
        return self

    def _paginated_colorings(self):
        page = self.cleaned_data.get('page') or 1
        paginator = Paginator(
            self._colorings,
            self.cleaned_data.get("per_page") or REST_FRAMEWORK["PAGE_SIZE"],
        )
        page_info = {
            'has_previous': paginator.get_page(page).has_previous(),
            'has_next': paginator.get_page(page).has_next(),
            'num_page': json.dumps(page),
        }
        self.result = {
            'page_info': page_info,
            'object_list': paginator.page(page).object_list,
            'page_range': ",".join([str(p) for p in paginator.page_range]),
            'theme': self._theme_presence
        }

    @property
    @lru_cache
    def _theme_presence(self):
        themes = Theme.objects.prefetch_related('likes').annotate(
            likes_count=Count('likes'),
            is_liked=(
                Exists(LikeTheme.objects.filter(theme=OuterRef('id'), user_id=self.cleaned_data['user_id']))
                if self.cleaned_data['user_id']
                else Value(False)
            )
        ).filter(id=self.cleaned_data['id'])
        if not themes.exists():
            raise ValidationError(
                message='Тематика не найдена.',
                response_status=status.HTTP_404_NOT_FOUND
            )
        return themes.first()

    @property
    def _colorings(self):
        return Coloring.objects.annotate(
            likes_count=Count('coloring_likes'),
            is_liked=(
                Exists(LikeColoring.objects.filter(
                    coloring=OuterRef('id'), user_id=self.cleaned_data['user_id']
                ))
                if self.cleaned_data['user_id']
                else Value(False)
            )
        ).filter(theme=self._theme_presence).order_by("-id")

    @lru_cache
    def _update_rating(self):
        theme = self._theme_presence
        theme.rating += 1
        theme.save()
