from django.core.mail import EmailMessage
from rest_framework import permissions, viewsets, status
from rest_framework import mixins, viewsets, filters
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import AdminStaffOnly, AdminOrReadOnly
from .serializers import (SignUpUserSerializer,
                          GetTokenSerializer,
                          CustomUserSerializer,
                          NotAdminSerializer)
from users.models import CustomUser, VerifyCode
from users import encoding


class ModelMixinSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, GenericViewSet):
    pass


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated, AdminStaffOnly, ]
    # выбираем поле для поиска вместо pk
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    # В каких полях ведётся поиск
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = CustomUserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = CustomUserSerializer(
                    request.user,
                    data=request.data,
                    # partial - отсутствие в запросе обязательных полей
                    # не приведёт к ошибке
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class SignUpUser(APIView):
    """
    Отправка кода верификации на email пользователя перед регистрацией
    Обязательные поля:
        - username
        - email
    P.S: функционал можно расширить, т.к. происходит прямая регистрация
        и код отправляется лишь единожды (можно установить срок жизник кода)
        и не регистрировать основную модель до его ввода
    """

    permission_classes = [permissions.AllowAny, ]

    # Добавим наш метод send_code_to_mail к классу EmailMessage
    @staticmethod
    def send_code_to_mail(user_data):
        mail = EmailMessage(
            subject=user_data['subject'],
            body=user_data['body'],
            from_email='my_practice_drf@api.ru',
            # в to, передаётся список адресов, поэтому
            # передадим списком один адрес
            to=[user_data['to_email']])
        mail.send()

    def post(self, request):
        serializer = SignUpUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        code = encoding.generate_code()
        VerifyCode.objects.create(
            username=user.username,
            email=user.email,
            code=encoding.encode_code(str(code)))
        text_email = (
            f'{user.username}, твой код '
            f'подтверждения: {code}')
        user_data = {
            'subject': 'Код подтверждения',
            'body': text_email,
            'to_email': user.email
        }
        self.send_code_to_mail(user_data)
        return Response(serializer.data, status.HTTP_200_OK)


class GetToken(APIView):
    """
    Получение JWT-токена в обмен на username и code,
    который был выслан по почте.
    Хеш кода в базе сравнивается с хешем переданного кода.
    """
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = CustomUser.objects.get(username=data['username'])
        except CustomUser.DoesNotExist:
            return Response(
                {'username': 'Такого пользователя не существует!'},
                status=status.HTTP_404_NOT_FOUND)
        try:
            user_verify_code = VerifyCode.objects.get(email=user.email)
        except VerifyCode.DoesNotExist:
            return Response(
                {'username': 'Такому пользователю не отправлялся '
                 'код подверждения. Повторите отправку!'},
                status=status.HTTP_404_NOT_FOUND)
        request_code = data.get('code')
        is_verifed = encoding.verify_code(
            request_code, user_verify_code.code)
        if is_verifed:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)
