from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
    Модель/таблица расширяет существующую таблицу пользователя
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200)

