# Generated by Django 4.0 on 2024-04-21 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0011_remove_favourite_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='like',
            options={'verbose_name': 'Like', 'verbose_name_plural': 'Likes'},
        ),
        migrations.RemoveField(
            model_name='like',
            name='like',
        ),
        migrations.AlterField(
            model_name='favourite',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='models_app.theme', verbose_name='Тематика'),
        ),
        migrations.AlterField(
            model_name='favourite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='models_app.user', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='like',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='models_app.theme', verbose_name='Тематика'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='models_app.user', verbose_name='Пользователь'),
        ),
    ]