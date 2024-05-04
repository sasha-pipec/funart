from django import forms
from rest_framework.generics import get_object_or_404
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from functools import lru_cache
from models_app.models import User, Theme
from models_app.models.theme_like.models import LikeTheme


class LikeCreateServices(ServiceWithResult):
    theme_id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        self.get_themes()
        self.like_search()
        self.like_create()
        return self

    @lru_cache
    def get_themes(self):
        return get_object_or_404(Theme, id=self.cleaned_data['theme_id'])

    def like_search(self):
        obj_like_search = LikeTheme.objects.filter(
            theme=self.get_themes(),
            user=self.cleaned_data['user'],
        )

        if obj_like_search.exists():
            raise Exception('The like already exists')

    def like_create(self):
        LikeTheme.objects.create(
            theme=self.get_themes(),
            user=self.cleaned_data['user'],

        )
