from django.contrib import admin

from models_app.models.favourite.models import Favourite


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_filter = ('theme', 'user')
    list_display = [
        "id",
        "theme",
        "user",
    ]
    list_display_links = (
        "id",
        "theme",
    )
