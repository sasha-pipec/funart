import json

from django.core.paginator import Paginator
from django.db.models import Count, OuterRef, Exists, Value
from service_objects.services import ServiceWithResult
from django import forms

from conf.settings.rest_framework import REST_FRAMEWORK
from models_app.models import Coloring, LikeColoring


class ColoringAllListService(ServiceWithResult):
    page = forms.IntegerField(required=False, min_value=1)
    per_page = forms.IntegerField(required=False, min_value=1)
    user_id = forms.IntegerField(required=False)

    def process(self):
        self._paginated_colorings()
        self.result = self._get_coloring_list
        return self

    def _paginated_colorings(self):
        page = self.cleaned_data.get('page') or 1
        paginator = Paginator(
            self._get_coloring_list,
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
    def _get_coloring_list(self):
        return Coloring.objects.annotate(
            likes_count=Count('coloring_likes'),
            is_liked=(
                Exists(LikeColoring.objects.filter(
                    coloring=OuterRef('id'),
                    user_id=self.cleaned_data['user_id']
                ))
                if self.cleaned_data['user_id']
                else Value(False)
            )
        ).all().order_by("-likes_count")
