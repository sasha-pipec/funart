# Generated by Django 4.0 on 2024-05-29 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserColoring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='themes/', verbose_name='Картинка темы')),
                ('coloring', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models_app.coloring', verbose_name='Раскраска')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models_app.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'User coloring',
                'verbose_name_plural': 'User coloring',
                'db_table': 'user_coloring',
            },
        ),
    ]
