import json
from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Count, Exists, OuterRef, Value
from rest_framework import status
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from conf.settings.rest_framework import REST_FRAMEWORK
from models_app.models import Theme, Category, LikeTheme

ORDER_BY = {
    ('rating', True): 'rating',
    ('rating', False): '-rating',
    ('updated_at', True): 'updated_at',
    ('updated_at', False): '-updated_at',
    ('likes_count', True): 'likes_count',
    ('likes_count', False): '-likes_count',
}


class ThemeListByCategoryService(ServiceWithResult):
    id = forms.IntegerField()
    page = forms.IntegerField(required=False, min_value=1)
    per_page = forms.IntegerField(required=False, min_value=1)
    user_id = forms.IntegerField(required=False)
    order_by = forms.CharField(required=False)

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
            raise NotFound(
                message="Такой категории не существует.",
                response_status=status.HTTP_404_NOT_FOUND
            )

    @property
    def _themes(self):
        if self._category:
            return Theme.objects.prefetch_related('likes').annotate(
                likes_count=Count('likes'),
                is_liked=Exists(LikeTheme.objects.filter(
                    theme=OuterRef('id'), user_id=self.cleaned_data["user_id"]
                ))
                if self.cleaned_data['user_id']
                else Value(False)
            ).filter(category__in=[self._category]).order_by("-updated_at").order_by(
                ORDER_BY.get((self.cleaned_data['order_by'], False), '-rating')
            )
