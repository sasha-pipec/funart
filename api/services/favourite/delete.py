from django import forms
from rest_framework.generics import get_object_or_404
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from models_app.models import User, Theme
from models_app.models.favourite.models import Favourite


class FavouriteDeleteServices(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        self.favourite_delete()
        return self

    def favourite_delete(self):
        obj_favourite_search = Favourite.objects.filter(
            theme=self.get_themes(),
            user=self.cleaned_data['user'],
        )
        if obj_favourite_search.exists():
            obj_favourite_search.first().delete()

    def get_themes(self):
        return get_object_or_404(Theme, id=self.cleaned_data['id'])
