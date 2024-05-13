# -*- coding: utf8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager


class User(AbstractUser):
    """Overriding the User model with the email field as primary"""

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
        app_label = "models_app"
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
