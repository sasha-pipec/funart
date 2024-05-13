# -*- coding: utf8 -*-
from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=255, verbose_name='Тематика')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to="themes/", verbose_name="Картинка темы")
    popular_image = models.ImageField(upload_to="themes/", verbose_name="Картинка темы для популярных")
    rating = models.IntegerField(default=0, verbose_name="Посещаемость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    category = models.ManyToManyField(to='Category', verbose_name='Категория')

    class Meta:
        db_table = 'themes'
        app_label = "models_app"
        verbose_name = 'Theme'
        verbose_name_plural = 'Themes'

    def __str__(self):
        return self.name
