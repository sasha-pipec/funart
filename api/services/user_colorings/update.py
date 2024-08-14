from django import forms
from service_objects.services import ServiceWithResult

from models_app.models import UserColoring


class UserColoringUpdateService(ServiceWithResult):
    user_id = forms.IntegerField()
    user_coloring_id = forms.IntegerField()
    coloring_json = forms.JSONField()
    image = forms.ImageField()

    def process(self):
        self.update()
        return self

    def update(self):
        user_coloring = UserColoring.objects.get(
            id=self.cleaned_data['user_coloring_id']
        )
        self.update_user_coloring(user_coloring)

    def update_user_coloring(self, user_coloring):
        user_coloring.image = self.cleaned_data['image']
        user_coloring.coloring_json = self.cleaned_data['coloring_json']
        user_coloring.save()
