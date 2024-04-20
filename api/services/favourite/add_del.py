from functools import lru_cache
from django import forms
from rest_framework.generics import get_object_or_404
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from models_app.models import User, Theme
from models_app.models.favourite.models import Favourite


class FavouriteServices(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        self.add_del_favourite()
        return self

    def add_del_favourite(self):
        obj_favourite = Favourite.objects.filter(
            theme=self.get_themes(),
            user=self.cleaned_data['user'],
        )
        if not obj_favourite.exists():
            Favourite.objects.create(
                theme=self.get_themes(),
                user=self.cleaned_data['user'],
                status=True
            )
        else:
            obj_favourite = obj_favourite.first()
            if obj_favourite.status == True:
                obj_favourite.status = False
                obj_favourite.save()
            else:
                obj_favourite.status = True
                obj_favourite.save()

    @lru_cache
    def get_themes(self):
        return get_object_or_404(Theme, id=self.cleaned_data['id'])
