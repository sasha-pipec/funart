from django.contrib import admin

from models_app.models.like.models import Like


@admin.register(Like)
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
