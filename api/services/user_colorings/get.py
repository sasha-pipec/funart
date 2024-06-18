from functools import lru_cache

from django import forms
from django.db.models import Count, Exists, OuterRef, Value
from rest_framework import status
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from models_app.models import UserColoring, Coloring, Theme, LikeTheme


class UserColoringGetService(ServiceWithResult):
    user_id = forms.IntegerField()
    user_coloring_id = forms.IntegerField()

    def process(self):
        self.result = {}
        self.result["object_list"] = self._user_coloring
        self.result["themes"] = self._see_more_themes
        return self

    @property
    @lru_cache()
    def _user_coloring(self):
        user_colorings = UserColoring.objects.filter(
            id=self.cleaned_data['user_coloring_id'],
            user_id=self.cleaned_data['user_id']
        )
        if not user_colorings.exists():
            raise NotFound(
                message='Раскрашенная hаскраска не найдена.',
                response_status=status.HTTP_404_NOT_FOUND
            )
        return user_colorings.first()

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

    @property
    def _get_coloring(self):
        return Coloring.objects.get(id=self._user_coloring.coloring.id)
