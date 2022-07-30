import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from users.models import CustomUser, VerifyCode
from reviews.models import Category, Comment, Genre, Review, Title


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Genre
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError(
                'Допускается оценка только от 1 до 10!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (request.method == 'POST'
           and Review.objects.filter(title=title, author=author).exists()):
            raise ValidationError('Вы уже оставляли свой отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
