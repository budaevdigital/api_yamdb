# Generated by Django 4.0.6 on 2022-07-29 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_verifycode'),
    ]

    operations = [
        migrations.AddField(
            model_name='verifycode',
            name='username',
            field=models.CharField(blank=True, max_length=150, verbose_name='username пользователя'),
        ),
    ]
