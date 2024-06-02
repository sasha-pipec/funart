import os
import random
import uuid
from functools import lru_cache

from django import forms
from rest_framework.exceptions import ValidationError
from service_objects.services import ServiceWithResult

from conf.settings.django import BASE_DIR
from models_app.models import Coloring, UserColoring


class UserColoringCreateUpdateService(ServiceWithResult):
    user_id = forms.IntegerField()
    coloring_id = forms.IntegerField()
    image = forms.ImageField()

    def process(self):
        self.update_or_create()
        return self

    def update_or_create(self):
        user_colorings = UserColoring.objects.filter(
            user_id=self.cleaned_data['user_id'],
            coloring=self._coloring
        )
        self.rename_user_coloring()
        if user_colorings.exists():
            return self.update_user_coloring(user_colorings.first())
        return self.create_user_coloring()

    def create_user_coloring(self):
        UserColoring.objects.create(
            user_id=self.cleaned_data['user_id'],
            coloring=self._coloring,
            image=self.cleaned_data['image']
        )

    def update_user_coloring(self, user_coloring):
        # Удаляем физически старый файл
        os.remove(os.path.join(BASE_DIR, user_coloring.image.url[1:]))
        user_coloring.image = self.cleaned_data['image']
        user_coloring.save()

    @property
    @lru_cache()
    def _coloring(self):
        obj_coloring = Coloring.objects.filter(id=self.cleaned_data['coloring_id'])
        if not obj_coloring.exists():
            raise ValidationError('The coloring with such data was not found')
        return obj_coloring.first()

    def rename_user_coloring(self):
        self.cleaned_data['image'].name = str(uuid.uuid4()) + '.jpg'
