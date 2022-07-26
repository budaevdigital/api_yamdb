from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from users.models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    @action(detail=True, methods=['post'])
    def create_user(self, request):
        # TODO - проверка: пользователь суперюзер - может создавать
        # пользователей с правами по-умолчанию, присваивается
        # обычная роль пользователей
        if self.serializer_class.is_valid():
            print('!!!!!!!!!!!!!!!')
            self.serializer_class.save()
            return Response(status=status.HTTP_201_CREATED)
        data = request.data
        print(data)
        print('!!!!!!!!!!!!!!!')
        return Response(status=status.HTTP_200_OK)
