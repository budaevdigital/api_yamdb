from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=50, required=True)
    email = serializers.EmailField(
        max_length=150,
        validators=[UniqueValidator(
            queryset=CustomUser.objects.all(),
            message='Пользователь с таким email уже существует')])
    # По-умолчанию, будет создана роль "пользователь"
    role = serializers.HiddenField(default=CustomUser.USER)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

    # TODO - сделать кастомную валидацию при создании пользователей
    # Например, количество символов

    # def create(self, validated_data):
    #     user = CustomUser.objects.create(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name']
    #     )
    #     user.save()
    #     return user
