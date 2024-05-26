import json

from django import forms
from django.core.paginator import Paginator
from django.db.models import Count, Value
from rest_framework.exceptions import ValidationError
from service_objects.services import ServiceWithResult

from conf.settings.rest_framework import REST_FRAMEWORK
from models_app.models import LikeColoring, Coloring
from models_app.models import User


class PersonalColoringListServices(ServiceWithResult):
    page = forms.IntegerField(required=False, min_value=1)
    per_page = forms.IntegerField(required=False, min_value=1)
    id = forms.IntegerField()

    def process(self):
        self._paginated_themes()
        return self

    def _paginated_themes(self):
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
        }


    @property
    def _colorings(self):
        like_coloring_id = (
            LikeColoring.objects
            .filter(user=self.cleaned_data['id'])
            .values_list('coloring_id', flat=True)
        )
        colorings = (
            Coloring.objects
            .annotate(
                likes_count=Count('coloring_likes'),
                is_liked=Value(True)
            )
            .filter(id__in=like_coloring_id)
        )
        return colorings
