# -*- coding: utf8 -*-
from django.db import models


class Favourite(models.Model):
    theme = models.ForeignKey(to='Theme', on_delete=models.CASCADE,
                              related_name='themes_favourites', verbose_name='Тематика')
    user = models.ForeignKey(to='User', on_delete=models.CASCADE,
                             related_name='favourites', verbose_name='Пользователь')

    def __str__(self):
        return self.theme.name

    class Meta:
        db_table = 'favourites'
        app_label = "models_app"
        verbose_name = 'Favourite'
        verbose_name_plural = 'Favourites'
