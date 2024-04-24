from rest_framework.generics import get_object_or_404
from service_objects.fields import ModelField
from functools import lru_cache
from django import forms

from service_objects.services import ServiceWithResult

from models_app.models import User, Theme
from models_app.models.like.models import Like


class AddLikeServices(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        self.add_like()
        return self

    def add_like(self):
        obj_like = Like.objects.filter(
            theme=self.get_themes(),
            user=self.cleaned_data['user'],
        )
        if not obj_like.exists():
            Like.objects.create(
                theme=self.get_themes(),
                user=self.cleaned_data['user'],
                like=True
            )
        else:
            obj_like.first().like = True
            obj_like.first().save()


    @lru_cache
    def get_themes(self):
        return get_object_or_404(Theme, id=self.cleaned_data['id'])
