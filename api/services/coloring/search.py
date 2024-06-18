import json
from django import forms
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator
from django.db.models import Q, Count, Exists, OuterRef, Value
from service_objects.services import ServiceWithResult

from conf.settings.rest_framework import REST_FRAMEWORK
from models_app.models import Theme, LikeTheme

ORDER_BY = {
    ('updated_at', True): 'updated_at',
    ('updated_at', False): '-updated_at',
    ('likes_count', True): 'likes_count',
    ('likes_count', False): '-likes_count',
}


class SearchService(ServiceWithResult):
    search = forms.CharField()
    page = forms.IntegerField(required=False, min_value=1)
    per_page = forms.IntegerField(required=False, min_value=1)
    user_id = forms.IntegerField(required=False)
    order_by = forms.CharField(required=False)

    def process(self):
        self._paginated_search()
        return self

    def _paginated_search(self):
        page = self.cleaned_data.get('page') or 1
        paginator = Paginator(
            self._search,
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
    def _search(self):
        themes = Theme.objects.annotate(
            similarity_name=TrigramSimilarity("name", self.cleaned_data["search"]),
            similarity_description=TrigramSimilarity("description", self.cleaned_data["search"]),
            likes_count=Count('likes'),
            is_liked=(
                Exists(LikeTheme.objects.filter(
                    theme=OuterRef('id'),
                    user_id=self.cleaned_data['user_id']
                ))
                if self.cleaned_data['user_id']
                else Value(False)
            )
        ).filter(
            Q(similarity_name__gt=0.3) |
            Q(similarity_description__gt=0.2)
        ).order_by(
            "-similarity_name", "-similarity_description",
            ORDER_BY.get((self.cleaned_data['order_by'], False), '-rating')
        )
        return themes
