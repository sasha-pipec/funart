# -*- coding: utf8 -*-
from django.db import models


class Like(models.Model):
    theme = models.ForeignKey(to='Theme', on_delete=models.CASCADE,
                              related_name='like_themes', verbose_name='Тематика')
    user = models.ForeignKey(to='User', on_delete=models.CASCADE,
                             related_name='like_users', verbose_name='Пользователь')
    like = models.BooleanField(default=None, verbose_name='Like')

    def __str__(self):
        return f'{self.theme} {self.like}'

    class Meta:
        db_table = 'like'
        app_label = "models_app"
        verbose_name = 'Like'
        verbose_name_plural = 'Like'
