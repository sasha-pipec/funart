from django.contrib import admin

from models_app.models.user_coloring.models import UserColoring


@admin.register(UserColoring)
class UserColoringAdmin(admin.ModelAdmin):
    list_filter = ('user', 'coloring', 'image')
    list_display = [
        'user',
        'coloring',
        'image',
    ]
    list_display_links = (
        'user',
        'coloring',
        'image',
    )
    ordering = (
        'user',
        'coloring',
        'image',
    )
