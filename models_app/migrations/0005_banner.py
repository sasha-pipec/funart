# Generated by Django 4.0 on 2024-07-18 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0004_usercoloring_coloring_json'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', models.CharField(max_length=255, verbose_name='Описание')),
                ('image', models.ImageField(upload_to='banner/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
                'db_table': 'banner',
            },
        ),
    ]
