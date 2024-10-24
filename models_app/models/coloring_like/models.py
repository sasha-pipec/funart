# -*- coding: utf8 -*-
from django.db import models


class LikeColoring(models.Model):
    coloring = models.ForeignKey(
        to='Coloring', on_delete=models.CASCADE,
        related_name='coloring_likes', verbose_name='Раскраска'
    )
    user = models.ForeignKey(
        to='User', on_delete=models.CASCADE,
        related_name='coloring_likes', verbose_name='Пользователь'
    )

    class Meta:
        unique_together = ('coloring', 'user',)
        db_table = 'coloring_likes'
        app_label = "models_app"
        verbose_name = 'Like coloring'
        verbose_name_plural = 'Likes colorings'

    def __str__(self):
        return self.coloring.name
