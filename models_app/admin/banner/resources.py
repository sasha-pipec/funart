from django.contrib import admin

from models_app.models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_filter = ('heading', 'description')
    list_display = [
        "id",
        "heading",
        "description",
        "image",

    ]
    list_display_links = (
        "id",
        "heading",
    )

