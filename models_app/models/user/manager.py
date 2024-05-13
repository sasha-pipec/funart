from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifiers for authentication instead of usernames."""
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Username not exists'))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
