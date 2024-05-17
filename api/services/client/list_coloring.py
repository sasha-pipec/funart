import json
from django import forms
from django.core.paginator import Paginator
from rest_framework.exceptions import ValidationError
from service_objects.services import ServiceWithResult
from conf.settings.rest_framework import REST_FRAMEWORK
from models_app.models import LikeTheme, LikeColoring
from models_app.models import User


class ClientColoringListServices(ServiceWithResult):
    page = forms.IntegerField(required=False, min_value=1)
    per_page = forms.IntegerField(required=False, min_value=1)
    id = forms.IntegerField()

    def process(self):
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

    def get_user(self):
        user_obj = User.objects.filter(id=self.cleaned_data['id'])
        if not user_obj.exists():
            raise ValidationError('The user with such data was not found')
        return user_obj.first()

    @property
    def _themes(self):
        coloring_likes = LikeColoring.objects.select_related('coloring').filter(user=self.get_user())
        return [coloring_like.coloring for coloring_like in coloring_likes]
