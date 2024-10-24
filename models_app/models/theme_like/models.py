# -*- coding: utf8 -*-
from django.db import models


class LikeTheme(models.Model):
    theme = models.ForeignKey(
        to='Theme', on_delete=models.CASCADE,
        related_name='likes', verbose_name='Тематика'
    )
    user = models.ForeignKey(
        to='User', on_delete=models.CASCADE,
        related_name='likes', verbose_name='Пользователь'
    )

    class Meta:
        unique_together = ('theme', 'user',)
        db_table = 'theme_likes'
        app_label = "models_app"
        verbose_name = 'Like theme'
        verbose_name_plural = 'Likes themes'

    def __str__(self):
        return self.theme.name
