
from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        print("creating  user")
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        print("created user=>>",user)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        print("creating super user")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(email, username, password, **extra_fields)
        print("created user=>>",user)
        return user


class CustomUser(AbstractUser):
    email = models.EmailField(
        _("Email Address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    objects = CustomUserManager()
