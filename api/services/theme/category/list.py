import json
from functools import lru_cache

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Count
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from conf.settings.rest_framework import REST_FRAMEWORK
from models_app.models import Theme, Category
from django import forms


class ThemeListByCategoryService(ServiceWithResult):
    id = forms.IntegerField()
    page = forms.IntegerField(required=False, min_value=1)
    per_page = forms.IntegerField(required=False, min_value=1)

    def process(self):
        self._paginated_themes()
        return self

    def _paginated_themes(self):
        page = self.cleaned_data.get("page") or 1
        paginator = Paginator(
            self._themes,
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
            'category': self._category,
            'page_range': ",".join([str(p) for p in paginator.page_range]),
        }

    @property
    @lru_cache
    def _category(self):
        try:
            return Category.objects.get(id=self.cleaned_data["id"])
        except ObjectDoesNotExist:
            raise NotFound(message="Такой категории не существует")

    @property
    def _themes(self):
        if self._category:
            return (
                Theme.objects
                .prefetch_related('likes')
                .annotate(likes_count=Count('likes'))
                .filter(category__in=[self._category])
                .order_by("-updated_at")
            )
