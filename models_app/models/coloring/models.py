# -*- coding: utf8 -*-
from django.db import models


class Coloring(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='colorings/', verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    theme = models.ForeignKey(
        to='Theme', on_delete=models.CASCADE,
        related_name='themes', verbose_name='Тематика'
    )

    class Meta:
        db_table = 'colorings'
        app_label = "models_app"
        verbose_name = 'Coloring'
        verbose_name_plural = 'Colorings'

    def __str__(self):
        return self.name
