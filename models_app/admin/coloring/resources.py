from django.contrib import admin

from models_app.models import Coloring, Theme
from django import forms


class ThemeFormAdmin(forms.ModelForm):
    theme = forms.ModelChoiceField(queryset=Theme.objects.all().distinct("id"), label="Тема")

    class Meta:
        model = Coloring
        fields = '__all__'


@admin.register(Coloring)
class ColoringAdmin(admin.ModelAdmin):
    list_filter = ("created_at",)
    list_display = [
        "id",
        "name",
        "image",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ["id", "created_at", "updated_at"]
    list_display_links = (
        "id",
        "name",
    )
    ordering = ("id", "theme", "created_at", "updated_at")
    form = ThemeFormAdmin
