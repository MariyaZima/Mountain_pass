from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from .models import *


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CoordsViewset(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImagesViewset(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class MountainViewset(viewsets.ModelViewSet):
    queryset = Mountain.objects.all()
    serializer_class = MountainSerializer
    filterset_fields = ('user__email',)

    def create(self, request, *args, **kwargs):
        serializer = MountainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Отправлено успешно',
                'id': serializer.data['id'],
            })
        if status.HTTP_400_BAD_REQUEST:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Bad Request',
                'id': None,
            })
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Ошибка подключения к базе данных',
                'id': None,
            })

    def partial_update(self, request, *args, **kwargs):
        mountain = self.get.object()
        if mountain.status == 'new':
            serializer = MountainSerializer(mountain, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'state': '1',
                    'message': 'Запись успешно изменена'
                })
            else:
                return Response({
                    'state': '0',
                    'message': serializer.errors
                })
        else:
            return Response({
                'state': '0',
                'message': f"Отклонено! Причина: {mountain.get_status_display()}"
            })

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        pass
