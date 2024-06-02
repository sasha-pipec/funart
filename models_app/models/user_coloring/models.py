from django.db import models


class UserColoring(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    coloring = models.ForeignKey('Coloring', on_delete=models.CASCADE, verbose_name='Раскраска')
    image = models.ImageField(upload_to="user_colorings/", verbose_name="Цветная раскраска")

    class Meta:
        db_table = 'image'
        app_label = "models_app"
        verbose_name = 'User coloring'
        verbose_name_plural = 'User coloring'

    def __str__(self):
        return f'{self.user.username} - {self.coloring.name}'
