from functools import lru_cache

from django import forms
from rest_framework.generics import get_object_or_404
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from models_app.models import User, LikeColoring, Coloring


class ColoringLikeCreateServices(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        self.get_coloring()
        self.like_search()
        self.like_create()
        return self

    @lru_cache
    def get_coloring(self):
        return get_object_or_404(Coloring, id=self.cleaned_data['id'])

    def like_search(self):
        obj_like_search = LikeColoring.objects.filter(
            coloring=self.get_coloring(),
            user=self.cleaned_data['user'],
        )
        if obj_like_search.exists():
            raise Exception('The like already exists')

    def like_create(self):
        LikeColoring.objects.create(
            coloring=self.get_coloring(),
            user=self.cleaned_data['user'],
        )


