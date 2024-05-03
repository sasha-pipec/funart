from django import forms
from rest_framework.generics import get_object_or_404
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User, Theme
from models_app.models.theme_like.models import LikeTheme


class LikeCreateServices(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        self.like_create()
        return self

    def like_create(self):
        obj_like_search = LikeTheme.objects.filter(
            theme=self.get_themes(),
            user=self.cleaned_data['user'],
        )
        if not obj_like_search.exists():
            LikeTheme.objects.create(
                theme=self.get_themes(),
                user=self.cleaned_data['user'],

            )

    def get_themes(self):
        return get_object_or_404(Theme, id=self.cleaned_data['id'])
