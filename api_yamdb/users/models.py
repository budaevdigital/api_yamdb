from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Модель пользователя с разными правами в зависимости от роли.
    Поля:
        - юзернейм
        - почта
        - имя
        - фамилия
        - обо мне
        - дата регистрации (авто)
        - роль
    В дополнительных методах класса, осуществяется
    проверка и возвращается boolean значение.
    """

    USER = 'User'
    MODERATOR = 'Moderator'
    ADMIN = 'Admin'

    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ'),
    )

    username = models.CharField(
        max_length=50, unique=True,
        help_text='Данный псевдоним будет виден другим пользователям',
        verbose_name='Ваш псевдоним')
    email = models.EmailField(
        max_length=150, unique=True,
        help_text='Введите ваш email',
        verbose_name='Email')
    first_name = models.CharField(
        max_length=50, blank=True,
        help_text='Введите ваше имя',
        verbose_name='Имя')
    last_name = models.CharField(
        max_length=50,
        help_text='Введите фамилию',
        verbose_name='Фамилия')
    bio = models.TextField(
        max_length=300, blank=True,
        help_text='Напишите пару слов о себе',
        verbose_name='Дополнительная информация')
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=15,
        choices=ROLES,
        default=USER)

    def __str__(self):
        return self.username

    def is_user(self):
        return self.role == self.USER

    def is_moderator(self):
        return self.role == self.MODERATOR

    def is_admin(self):
        return self.role == self.ADMIN

    class Meta():
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
