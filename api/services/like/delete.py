from django import forms
from rest_framework.generics import get_object_or_404
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User, Theme
from models_app.models.like.models import LikeTheme


class LikeDeleteServices(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        self.like_delete()
        return self

    def like_delete(self):
        obj_like_search = LikeTheme.objects.filter(
            theme=self.get_themes(),
            user=self.cleaned_data['user'],
        )
        if obj_like_search.exists():
            obj_like_search.first().delete()

    def get_themes(self):
        return get_object_or_404(Theme, id=self.cleaned_data['id'])
