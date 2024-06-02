import json

from django import forms
from django.core.paginator import Paginator
from service_objects.services import ServiceWithResult

from conf.settings.rest_framework import REST_FRAMEWORK
from models_app.models import UserColoring


class UserColoringsListServices(ServiceWithResult):
    user_id = forms.IntegerField()

    def process(self):
        self._paginated_colorings()
        return self

    def _paginated_colorings(self):
        page = self.cleaned_data.get('page') or 1
        paginator = Paginator(
            self._user_colorings,
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
    def _user_colorings(self):
        return UserColoring.objects.filter(user=self.cleaned_data['user_id'])


