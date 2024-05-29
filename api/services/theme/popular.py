from django.db.models import Count, Exists, OuterRef, Value
from django import forms
from service_objects.services import ServiceWithResult

from models_app.models import Theme, LikeTheme


class ThemePopularListServices(ServiceWithResult):
    user_id = forms.IntegerField(required=False)

    def process(self):
        self.result = self._popular_themes
        return self

    @property
    def _popular_themes(self):
        return Theme.objects.prefetch_related('likes').annotate(
            likes_count=Count('likes'),
            is_liked=(
                Exists(LikeTheme.objects.filter(theme=OuterRef('id'), user_id=self.cleaned_data['user_id']))
                if self.cleaned_data['user_id']
                else Value(False)
            )
        ).order_by("-rating")[:4]
