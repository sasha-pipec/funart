from django.db import models


class Banner(models.Model):
    heading = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.CharField(max_length=255, verbose_name='Описание')
    image = models.ImageField(upload_to='banner/', verbose_name='Изображение')


    class Meta:
        db_table = 'banner'
        app_label = "models_app"
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'

    def __str__(self):
        return self.heading
