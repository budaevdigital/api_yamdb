# Generated by Django 4.0.6 on 2022-07-23 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(help_text='Введите ваш email', max_length=150, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(help_text='Данный псевдоним будет виден другим пользователям', max_length=50, verbose_name='Ваш псевдоним'),
        ),
    ]