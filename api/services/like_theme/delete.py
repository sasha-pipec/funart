from django import forms
from rest_framework.generics import get_object_or_404
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User, Theme
from models_app.models.theme_like.models import LikeTheme


class LikeDeleteService(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        self.like_delete()
        return self

    def like_delete(self):
        likes = LikeTheme.objects.filter(
            theme=self._theme,
            user=self.cleaned_data['user'],
        )
        if likes.exists():
            likes.first().delete()

    @property
    def _theme(self):
        return get_object_or_404(Theme, id=self.cleaned_data['id'])
