from django import forms
from django.db.models import Count, OuterRef, Exists, Value
from service_objects.services import ServiceWithResult

from models_app.models import Coloring, LikeColoring


class ColoringGetService(ServiceWithResult):
    id = forms.IntegerField()
    user_id = forms.IntegerField(required=False)

    def process(self):
        self.result = self._get_coloring
        return self

    @property
    def _get_coloring(self):
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
        ).get(id=self.cleaned_data['id'])
