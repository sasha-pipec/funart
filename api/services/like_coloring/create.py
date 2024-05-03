from django import forms
from rest_framework.generics import get_object_or_404
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from models_app.models import User, LikeColoring, Coloring


class ColoringLikeCreateServices(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        self.like_create()
        return self

    def like_create(self):
        obj_like_search = LikeColoring.objects.filter(
            coloring=self.get_themes(),
            user=self.cleaned_data['user'],
        )
        if not obj_like_search.exists():
            LikeColoring.objects.create(
                coloring=self.get_themes(),
                user=self.cleaned_data['user'],

            )

    def get_themes(self):
        return get_object_or_404(Coloring, id=self.cleaned_data['id'])
