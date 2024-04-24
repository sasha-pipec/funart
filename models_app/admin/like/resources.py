from django.contrib import admin

from models_app.models.like.models import LikeTheme


@admin.register(LikeTheme)
class LikeAdmin(admin.ModelAdmin):
    #list_filter = ('theme', 'user')
    list_display = [
        "id",
        "theme",
        "user",
    ]
    # #list_display_links = (
    #     "id",
    #     "theme",
    # )
