from django import forms
from rest_framework.generics import get_object_or_404
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User, LikeColoring, Coloring


class ColoringLikeDeleteService(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        self.like_delete()
        return self

    def like_delete(self):
        likes = LikeColoring.objects.filter(
            theme=self._coloring,
            user=self.cleaned_data['user'],
        )
        if likes.exists():
            likes.first().delete()

    @property
    def _coloring(self):
        return get_object_or_404(Coloring, id=self.cleaned_data['id'])
