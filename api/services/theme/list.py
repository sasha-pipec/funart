from django import forms
from django.db.models import Count, Exists, OuterRef, Value
from service_objects.services import ServiceWithResult

from models_app.models import Theme, LikeTheme
from utils.paginator import paginated_queryset

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
        self.result = paginated_queryset(
            queryset=self._themes,
            page=self.cleaned_data.get("page"),
            per_page=self.cleaned_data.get("per_page")
        )

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
