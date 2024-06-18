from django import forms
from django.db.models import Count, Exists, OuterRef, Value
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User, LikeTheme, Theme
from utils.paginator import paginated_queryset

ORDER_BY = {
    ('rating', True): 'rating',
    ('rating', False): '-rating',
    ('updated_at', True): 'updated_at',
    ('updated_at', False): '-updated_at',
    ('likes_count', True): 'likes_count',
    ('likes_count', False): '-likes_count',
}


class ThemePersonalListService(ServiceWithResult):
    user = ModelField(User)
    page = forms.IntegerField(required=False, min_value=1)
    per_page = forms.IntegerField(required=False, min_value=1)
    order_by = forms.CharField(required=False)
    direction = forms.BooleanField(required=False)

    def process(self):
        self.result = self._themes_personal
        return self

    @property
    def _themes_personal(self):
        liked_themes = self._liked_themes
        categories_themes = liked_themes.values_list("theme__category__id", flat=True).distinct()
        recommend_themes = Theme.objects.prefetch_related('likes').annotate(
            likes_count=Count('likes'),
            is_liked=(
                Exists(LikeTheme.objects.filter(
                    theme=OuterRef('id'), user_id=self.cleaned_data['user'].id
                ))
                if self.cleaned_data['user'].id
                else Value(False)
            )
        ).filter(
            category__id__in=categories_themes
        ).exclude(
            id__in=liked_themes
        ).order_by(
            ORDER_BY.get((self.cleaned_data['order_by'], self.cleaned_data['direction']), '-rating')
        )
        return paginated_queryset(
            queryset=recommend_themes,
            page=self.cleaned_data.get("page"),
            per_page=self.cleaned_data.get("per_page")
        )

    @property
    def _liked_themes(self):
        return LikeTheme.objects.filter(user=self.cleaned_data["user"])
