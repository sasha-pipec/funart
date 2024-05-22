from models_app.models import LikeColoring, LikeTheme
from django.contrib import admin


@admin.register(LikeColoring)
class LikeColorinAgdmin(admin.ModelAdmin):
    list_display = [
        'coloring', 'user'
    ]


@admin.register(LikeTheme)
class LikeThemeAdmin(admin.ModelAdmin):
    list_display = [
        'theme', 'user'
    ]
