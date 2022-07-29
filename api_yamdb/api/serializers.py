from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import CustomUser, VerifyCode
import re


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('__all__')
        # fields = ('username', 'email',
        #           'first_name', 'last_name',
        #           'bio', 'role')
        read_only_fields = ('role',)


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')


class SignUpUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=50, required=True)
    email = serializers.EmailField(
        max_length=150,
        validators=[UniqueValidator(
            queryset=CustomUser.objects.all(),
            message='Пользователь с таким email уже существует')])

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def validate_username(self, value):
        if not re.match("^[a-zA-Z\d\@\.\+\-\_]*$", value):
            raise serializers.ValidationError('Поле username содержит '
                                              'запрещёные символы. '
                                              'Введите другой username')
        return value


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True, source='code')

    class Meta:
        model = VerifyCode
        fields = (
            'username',
            'confirmation_code')
