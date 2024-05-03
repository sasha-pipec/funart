from django.contrib import admin

from models_app.models import LikeColoring
from models_app.models.theme_like.models import LikeTheme


@admin.register(LikeTheme)
class LikeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "theme",
        "user",
    ]



@admin.register(LikeColoring)
class LikeColoringAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "coloring",
        "user",
    ]