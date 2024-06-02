from functools import lru_cache

from django import forms
from rest_framework import status
from rest_framework.generics import get_object_or_404
from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from models_app.models import User, LikeColoring, Coloring


class ColoringLikeCreateService(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        self.like_presence()
        self.like_create()
        return self

    @property
    @lru_cache
    def _coloring(self):
        return get_object_or_404(Coloring, id=self.cleaned_data['id'])

    def like_presence(self):
        obj_like_search = LikeColoring.objects.filter(
            coloring=self._coloring,
            user=self.cleaned_data['user'],
        )
        if obj_like_search.exists():
            raise ValidationError(
                message='Вы уже оценили эту раскраску.',
                response_status=status.HTTP_400_BAD_REQUEST
            )

    def like_create(self):
        LikeColoring.objects.create(
            coloring=self._coloring,
            user=self.cleaned_data['user'],
        )
