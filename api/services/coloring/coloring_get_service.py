from functools import lru_cache

from django import forms
from django.db.models import Count, OuterRef, Exists, Value
from service_objects.services import ServiceWithResult
from django.shortcuts import get_object_or_404

from models_app.models import Coloring, LikeColoring, Theme, LikeTheme


class ColoringGetService(ServiceWithResult):
    id = forms.IntegerField()
    user_id = forms.IntegerField(required=False)

    def process(self):
        self._present()
        # self._coloring_presence()
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
        '''получаем id темы'''
        theme_id = self.get_theme_id()
        '''получаем все раскраски темы theme_id'''
        colorings_id_list = self.get_colorings_id_list(theme_id)
        '''получаем индекс нужной раскраски в писке colorings_id_list'''
        index_coloring = colorings_id_list.index(self.cleaned_data['id'])

        next_coloring = self._get_next_coloring(theme_id, colorings_id_list, index_coloring)
        previous_coloring = self._get_previous_coloring(theme_id, colorings_id_list, index_coloring)
        return next_coloring, previous_coloring

    def _get_next_coloring(self, theme_id, colorings_id_list, index_coloring):
        '''если наша раскраска находится в конце списка раскрасок, то:'''
        if index_coloring == len(colorings_id_list) - 1:
            '''получаем первую раскраску следующей темы'''
            return self.get_first_coloring_from_the_next_theme(theme_id)
        return colorings_id_list[index_coloring + 1]

    def get_first_coloring_from_the_next_theme(self, theme_id):
        '''список всех id тем'''
        theme_all_id = self.get_list_id_all_theme()
        '''узнаём индекс темы в списке theme_all_id'''
        index_theme = theme_all_id.index(theme_id)
        '''получаем индекс первой темы'''
        next_theme_id = theme_all_id[0]
        '''если наша тема не последняя в списке'''
        if index_theme != len(theme_all_id) - 1:
            '''берём следующую тему'''
            next_theme_id = theme_all_id[index_theme + 1]
        '''получаем список всех раскрасок следующей темы'''
        colorings_id_list = self.get_colorings_id_list(next_theme_id)
        if colorings_id_list:
            return list(colorings_id_list)[0]
        return self.get_first_coloring_from_the_next_theme(next_theme_id)

    def _get_previous_coloring(self, theme_id, colorings_id_list, index_coloring):
        if index_coloring == 0:
            return self.get_latest_coloring_from_the_previous_theme(theme_id)
        return colorings_id_list[index_coloring - 1]

    def get_latest_coloring_from_the_previous_theme(self, theme_id):
        '''получаем список всех тем'''
        theme_all_id = self.get_list_id_all_theme()
        '''узнаём индекс темы в списке theme_all_id'''
        index_theme = theme_all_id.index(theme_id)
        '''получаем индекс предыдущей темы'''
        previous_theme_id = theme_all_id[index_theme - 1]
        '''если индекс темы имеет индекс 0'''
        if index_theme == 0:
            '''если index_theme == 0, то выбираем предпоследнюю тему'''
            '''хотя theme_all_id[0 - 1] = theme_all_id[-1]'''
            '''лишнее условие?'''
            previous_theme_id = theme_all_id[-1]
        '''получаем список раскрасок с предыдущей темы'''
        colorings_id_list = self.get_colorings_id_list(previous_theme_id)
        if colorings_id_list:
            '''возвращаем последний id предыдущей темы'''
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
        '''если есть id темы, зачем '''
        e = Theme.objects.filter(id=theme_id).first()
        '''получаем все раскраски с темой theme_id'''
        w = Theme.objects.filter(id=theme_id).first().themes
        '''получаем список id всех раскрасок с темой theme_id'''
        r = Theme.objects.filter(id=theme_id).first().themes.values_list("id", flat=True)
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
        ).exclude(
            id=self.get_theme_id()
        ).order_by('-updated_at')[:6]

    # def _coloring_presence(self):
    #     colorings = Coloring.objects.filter(id=self.cleaned_data["id"])
    #     if not colorings.exists():
    #         raise NotFound(message="Раскраска не найдена.", response_status=404)
    #     return colorings.first()

    def _present(self):
        coloring = get_object_or_404(Coloring, id=self.cleaned_data['id'])
        return coloring
