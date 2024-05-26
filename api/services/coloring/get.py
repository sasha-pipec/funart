from django import forms
from django.db.models import Count, OuterRef, Exists, Value
from rest_framework.exceptions import ValidationError
from service_objects.services import ServiceWithResult

from models_app.models import Coloring, LikeColoring, User


class ColoringGetServices(ServiceWithResult):
    id = forms.IntegerField()
    user_id = forms.IntegerField(required=False)

    def process(self):
        self.result = self._get_coloring
        return self

    @property
    def _user(self):
        user_obj = User.objects.filter(id=self.cleaned_data['user_id'])
        if not user_obj.exists():
            raise ValidationError('The user with such data was not found')
        return user_obj.first()

    @property
    def _get_coloring(self):
        return Coloring.objects.annotate(
            likes_count=Count('coloring_likes'),
            is_liked=(
                Exists(LikeColoring.objects.filter(coloring=OuterRef('id'), user=self._user))
                if self.cleaned_data['id']
                else Value(False)
            )
        ).get(id=self.cleaned_data['id'])
