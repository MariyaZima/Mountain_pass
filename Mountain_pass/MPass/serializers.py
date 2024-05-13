from drf_writable_nested import WritableNestedModelSerializer
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImagesSerializer(serializers.ModelSerializer):
    data = serializers.URLField()

    class Meta:
        model = Images
        fields = ['data', 'title']


class MountainSerializer(WritableNestedModelSerializer):
    add_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    user = UserSerializer()
    coord = CoordsSerializer()
    level = LevelSerializer(allow_null=True)
    images = ImagesSerializer(many=True)
    status = serializers.CharField()

    class Meta:
        model = Mountain
        fields = ['id',
                  'status',
                  'add_time',
                  'beauty_title',
                  'title',
                  'other_titles',
                  'connect',
                  'user',
                  'coord',
                  'level',
                  'images'
            ]

    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        coord = validated_data.pop('coord')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        user, created = User.objects.get_or_create(**user)

        coord = Coords.objects.create(**coord)
        level = Level.objects.create(**level)
        mountain = Mountain.objects.create(**validated_data, user=user, coord=coord, level=level, status='new')

        for image in images:
            data = image.pop('img')
            title = image.pop('title')
            Images.objects.create(img=data, perevaladded=mountain, title=title)

        return mountain

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_user_fields = [
                instance_user.name != data_user['name'],
                instance_user.fam != data_user['fam'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError({'Отклонено': 'Нельзя изменять данные пользователя'})
        return data
