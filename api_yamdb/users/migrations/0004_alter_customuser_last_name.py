# Generated by Django 4.0.6 on 2022-07-23 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_user_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, help_text='Введите фамилию', max_length=50, verbose_name='Фамилия'),
        ),
    ]