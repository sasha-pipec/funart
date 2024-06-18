import io
import os
import sys

import numpy as np

from django.contrib import admin
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import post_save
from django.dispatch import receiver

from models_app.models import Theme, Coloring


class ColoringInline(admin.TabularInline):
    model = Coloring
    extra = 10


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_filter = ('name', 'created_at')
    list_display = [
        "id",
        "name",
        "description",
        "rating",
        'image',
        "created_at",
        "updated_at",
    ]
    list_display_links = (
        "id",
        "name",
    )
    ordering = ("id", "created_at", "updated_at")
    filter_horizontal = ['category', ]
    inlines = [ColoringInline, ]

    @receiver(post_save, sender=Theme)
    def convert_to_png(**kwargs):
        colorings = kwargs["instance"].themes.all()
        for coloring in colorings:
            image_type = coloring.image.name.split(".")[-1]
            if image_type != "png":
                pillow_image = Image.open(coloring.image.path)
                pillow_image = pillow_image.convert("RGBA")

                image_np_array = np.array(pillow_image)

                white = np.sum(image_np_array[:, :, :3], axis=2)
                white_mask = np.where(white >= 200 * 3, 1, 0)
                alpha = np.where(white_mask, 0, image_np_array[:, :, -1])
                image_np_array[:, :, -1] = alpha

                pillow_png_image = Image.fromarray(np.uint8(image_np_array))

                output = io.BytesIO()
                path_to_old_image = coloring.image.path

                pillow_png_image.save(output, "PNG")
                png_image = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    coloring.image.name.split(".")[-2] + ".png",
                    'image/png',
                    sys.getsizeof(pillow_png_image), None
                )
                coloring.image = png_image
                coloring.save()
                os.remove(path_to_old_image)

