import json
from functools import lru_cache

from django import forms
from django.core.paginator import Paginator
from django.db.models import Count, Exists, OuterRef, Value
from rest_framework.exceptions import ValidationError
from service_objects.services import ServiceWithResult

from conf.settings.rest_framework import REST_FRAMEWORK
from models_app.models import Coloring, Theme, User, LikeTheme, LikeColoring


class ColoringListServices(ServiceWithResult):
    page = forms.IntegerField(required=False, min_value=1)
    per_page = forms.IntegerField(required=False, min_value=1)
    id = forms.IntegerField()
    user_id = forms.IntegerField(required=False)

    def process(self):
        self._paginated_colorings()
        self._update_rating()
        return self

    def _paginated_colorings(self):
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
    def _user(self):
        user_obj = User.objects.filter(id=self.cleaned_data['user_id'])
        if not user_obj.exists():
            raise ValidationError('The user with such data was not found')
        return user_obj.first()

    @property
    def _colorings(self):
        return (
            Coloring.objects
            .annotate(
                likes_count=Count('coloring_likes'),
                is_liked=(
                    Exists(LikeColoring.objects.filter(coloring=OuterRef('id'), user=self._user))
                    if self.cleaned_data['user_id']
                    else Value(False)
                )
            )
            .filter(theme_id=self.cleaned_data["id"])
            .order_by("-id")
        )

    @lru_cache
    def _update_rating(self):
        theme = Theme.objects.get(id=self.cleaned_data["id"])
        theme.rating += 1
        theme.save()
