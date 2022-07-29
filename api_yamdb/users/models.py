from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'User'
MODERATOR = 'Moderator'
ADMIN = 'Admin'

ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Админ'),
)


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

    username = models.CharField(
        max_length=150,
        help_text='Данный псевдоним будет виден другим пользователям',
        verbose_name='Ваш псевдоним')
    email = models.EmailField(
        max_length=254, unique=True,
        help_text='Введите ваш email',
        verbose_name='Email')
    first_name = models.CharField(
        max_length=150, blank=True,
        help_text='Введите ваше имя',
        verbose_name='Имя')
    last_name = models.CharField(
        max_length=150, blank=True,
        help_text='Введите фамилию',
        verbose_name='Фамилия')
    bio = models.TextField(
        max_length=500, blank=True,
        help_text='Напишите пару слов о себе',
        verbose_name='Дополнительная информация')
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=15,
        choices=ROLES,
        default=USER)

    # в нашей модели, привязка будет по полю email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN

    class Meta():
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # проверка на уникальность полей
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]


class VerifyCode(models.Model):
    username = models.CharField(
        max_length=150,
        verbose_name='username пользователя',
        blank=True)
    email = models.EmailField(verbose_name='email пользователя', blank=True)
    # хранится не код, а его хеш
    code = models.BinaryField(verbose_name='Код верификации')
    add_time = models.DateTimeField(
        verbose_name='Когда сгенерирован код ', auto_now_add=True)
