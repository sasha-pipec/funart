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
        next_coloring, previous_coloring = self._get_navigation
        return Coloring.objects.select_related("theme").annotate(
            likes_count=Count('coloring_likes'),
            is_liked=(
                Exists(LikeColoring.objects.filter(
                    coloring=OuterRef('id'),
                    user_id=self.cleaned_data['user_id']
                ))
                if self.cleaned_data['user_id']
                else Value(False)
            ),
            next=Value(next_coloring),
            previous=Value(previous_coloring)
        ).get(id=self.cleaned_data['id'])

    @property
    def _get_navigation(self):
        theme_id = self.get_theme_id()
        colorings_id_list = self.get_colorings_id_list(theme_id)
        index_coloring = colorings_id_list.index(self.cleaned_data['id'])
        next_coloring = self._get_next_coloring(theme_id, colorings_id_list, index_coloring)
        previous_coloring = self._get_previous_coloring(theme_id, colorings_id_list, index_coloring)
        return next_coloring, previous_coloring

    def _get_next_coloring(self, theme_id, colorings_id_list, index_coloring):
        if index_coloring == len(colorings_id_list) - 1:
            return self.get_first_coloring_from_the_next_theme(theme_id)
        return colorings_id_list[index_coloring + 1]

    def get_first_coloring_from_the_next_theme(self, theme_id):
        theme_all_id = self.get_list_id_all_theme()
        index_theme = theme_all_id.index(theme_id)
        next_theme_id = theme_all_id[0]
        if index_theme != len(theme_all_id) - 1:
            next_theme_id = theme_all_id[index_theme + 1]
        colorings_id_list = self.get_colorings_id_list(next_theme_id)
        if colorings_id_list:
            return list(colorings_id_list)[0]
        return self.get_first_coloring_from_the_next_theme(next_theme_id)

    def _get_previous_coloring(self, theme_id, colorings_id_list, index_coloring):
        if index_coloring == 0:
            return self.get_latest_coloring_from_the_previous_theme(theme_id)
        return colorings_id_list[index_coloring - 1]

    def get_latest_coloring_from_the_previous_theme(self, theme_id):
        theme_all_id = self.get_list_id_all_theme()
        index_theme = theme_all_id.index(theme_id)
        previous_theme_id = theme_all_id[index_theme - 1]
        if index_theme == 0:
            previous_theme_id = theme_all_id[-1]
        colorings_id_list = self.get_colorings_id_list(previous_theme_id)
        if colorings_id_list:
            return list(colorings_id_list)[-1]
        return self.get_latest_coloring_from_the_previous_theme(previous_theme_id)

    @lru_cache
    def get_theme_id(self):
        return Coloring.objects.filter(id=self.cleaned_data['id']).first().theme.id

    @staticmethod
    @lru_cache
    def get_list_id_all_theme():
        return list(Theme.objects.values_list("id", flat=True))

    @staticmethod
    def get_colorings_id_list(theme_id):
        return list(Theme.objects.filter(id=theme_id).first().themes.values_list("id", flat=True))

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
