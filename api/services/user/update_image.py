from functools import lru_cache

from django import forms
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User


class UserUpdateService(ServiceWithResult):
    user = ModelField(User)
    image = forms.ImageField(required=False)

    def process(self):
        self.update_user()
        return self


    @property
    @lru_cache
    def _user(self):
        return self.cleaned_data['user']

    def update_user(self):
        if self._user.image:
            self._user.image.delete()
        self._user.image = self.cleaned_data['image']
        self._user.save()
