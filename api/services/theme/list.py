import json

from django import forms
from django.core.paginator import Paginator
from django.db.models import Count, Exists, OuterRef, Value
from service_objects.services import ServiceWithResult

from conf.settings.rest_framework import REST_FRAMEWORK
from models_app.models import Theme, LikeTheme

ORDER_BY = {
    ('rating', True): 'rating',
    ('rating', False): '-rating',
    ('updated_at', True): 'updated_at',
    ('updated_at', False): '-updated_at',
    ('likes_count', True): 'likes_count',
    ('likes_count', False): '-likes_count',
}


class ThemeListService(ServiceWithResult):
    page = forms.IntegerField(required=False, min_value=1)
    per_page = forms.IntegerField(required=False, min_value=1)
    user_id = forms.IntegerField(required=False)
    order_by = forms.CharField(required=False)
    direction = forms.BooleanField(required=False)

    def process(self):
        if not self.cleaned_data["order_by"]:
            self.cleaned_data["order_by"] = "updated_at"
        if not self.cleaned_data["direction"]:
            self.cleaned_data["direction"] = False
        self._paginated_themes()
        return self

    def _paginated_themes(self):
        page = self.cleaned_data.get('page') or 1
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
            'page_range': ",".join([str(p) for p in paginator.page_range]),
        }

    @property
    def _themes(self):
        return Theme.objects.prefetch_related('likes').annotate(
            likes_count=Count('likes'),
            is_liked=(
                Exists(LikeTheme.objects.filter(
                    theme=OuterRef('id'), user_id=self.cleaned_data['user_id']
                ))
                if self.cleaned_data['user_id']
                else Value(False)
            )
        ).order_by(
            ORDER_BY.get((self.cleaned_data['order_by'], self.cleaned_data['direction']), '-rating')
        )
