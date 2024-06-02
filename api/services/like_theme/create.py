from django import forms
from rest_framework import status
from rest_framework.generics import get_object_or_404
from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from functools import lru_cache
from models_app.models import User, Theme
from models_app.models.theme_like.models import LikeTheme


class LikeCreateService(ServiceWithResult):
    theme_id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        self.like_presence()
        self.like_create()
        return self

    @property
    @lru_cache
    def _theme(self):
        return get_object_or_404(Theme, id=self.cleaned_data['theme_id'])

    def like_presence(self):
        likes = LikeTheme.objects.filter(
            theme=self._theme,
            user=self.cleaned_data['user'],
        )
        if likes.exists():
            raise ValidationError(
                message='Вы уже поставили лайк на эту тематику.',
                response_status=status.HTTP_400_BAD_REQUEST
            )

    def like_create(self):
        LikeTheme.objects.create(
            theme=self._theme,
            user=self.cleaned_data['user'],
        )
