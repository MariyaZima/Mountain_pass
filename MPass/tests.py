import status
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Mountain, User, Coords, Level
from .serializers import MountainSerializer


class MountainApiTestCase(APITestCase):
    def setUp(self):
        self.mountain_1 = Mountain.objects.create(
            beauty_title='Beauty title 1',
            title='Title 1',
            other_titles='Other titles 1',
            connect='',
            add_time='24-05-2024 19:18:20',
            user=User.objects.create(
                email='user1@mail.ru',
                fam='fam 1',
                name='name 1',
                otc='otc 1',
                phone='+78000000000'
            ),
            coord=Coords.objects.create(
                latitude='11.11111',
                longitude='22.22222',
                height='1111'
            ),
            level=Level.objects.create(
                winter='1A',
                summer='1A',
                autumn='1A',
                spring='1A',
            ),
            status='new'
        )
        self.mountain_2 = Mountain.objects.create(
            beauty_title='Beauty title 2',
            title='Title 2',
            other_titles='Other titles 2',
            connect='',
            add_time='24-05-2024 21:02:02',
            user=User.objects.create(
                email='user1@mail.ru',
                fam='fam 2',
                name='name 2',
                otc='otc 2',
                phone='+78000000001'
            ),
            coord=Coords.objects.create(
                latitude='33.33333',
                longitude='44.44444',
                height='2222'
            ),
            level=Level.objects.create(
                winter='2A',
                summer='2A',
                autumn='2A',
                spring='2A',
            ),
            status='new'
        )

    def test_get(self):
        url = reverse('mountain-list')
        response = self.client.get(url)
        serializer_data = MountainSerializer([self.mountain_1, self.mountain_2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


# python manage.py test . - запустить все тесты


class MountainSerializerTestCase(TestCase):
    def setUp(self):
        self.mountain_1 = Mountain.objects.create(
            beauty_title='Beauty title 1',
            title='Title 1',
            other_titles='Other titles 1',
            connect='',
            add_time='',
            user=User.objects.create(
                email='user1@mail.ru',
                fam='fam 1',
                name='name 1',
                otc='otc 1',
                phone='+78000000000'
            ),
            coord=Coords.objects.create(
                latitude='11.11111',
                longitude='22.22222',
                height='1111'
            ),
            level=Level.objects.create(
                winter='1A',
                summer='1A',
                autumn='1A',
                spring='1A',
            ),
            status=''
        )
        self.mountain_2 = Mountain.objects.create(
            beauty_title='Beauty title 2',
            title='Title 2',
            other_titles='Other titles 2',
            connect='',
            add_time='',
            user=User.objects.create(
                email='user1@mail.ru',
                fam='fam 2',
                name='name 2',
                otc='otc 2',
                phone='+78000000001'
            ),
            coord=Coords.objects.create(
                latitude='33.33333',
                longitude='44.44444',
                height='2222'
            ),
            level=Level.objects.create(
                winter='2A',
                summer='2A',
                autumn='2A',
                spring='2A',
            ),
            status=''
        )

    def test_check(self):
        serializer_data = MountainSerializer([self.mountain_1, self.mountain_2], many=True).data
        expected_data = [
            {
                'id': 1,
                'status': '',
                'add_time': str(self.mountain_1.add_time.strftime(format="%d-%m-%Y %H:%M:%S")),
                "beauty_title": "Beauty title 1",
                'title': 'Title 1',
                'other_titles': 'Other titles 1',
                'connect': '',
                "user": {
                    'email': 'user1@mail.ru',
                    'fam': 'fam 1',
                    'name': 'name 1',
                    'otc': 'otc 1',
                    'phone': '+78000000000'
                },
                "coord": {
                    'latitude': 11.11111,
                    'longitude': 22.22222,
                    'height': 1111
                },
                'level': {
                    'winter': '1A',
                    'summer': '1A',
                    'autumn': '1A',
                    'spring': '1A',
                },
                "images": [],
            },
            {
                'id': 2,
                "status": "",
                'add_time': self.mountain_2.add_time.strftime(format="%d-%m-%Y %H:%M:%S"),
                "beauty_title": "Beauty title 2",
                "title": "Title 2",
                "other_titles": "Other titles 2",
                "connect": '',
                "user": {
                    "email": "user1@mail.ru",
                    "fam": "fam 2",
                    "name": "name 2",
                    "otc": "otc 2",
                    "phone": "+78000000001",
            },
                "coord": {
                    "latitude": 33.33333,
                    "longitude": 44.44444,
                    "height": 2222
            },
                "level": {
                    "winter": "2A",
                    "summer": "2A",
                    "autumn": "2A",
                    "spring": "2A",
            },
                "images": [],
        },

        ]
        #print('-------------------------')
        #print(serializer_data)
        #print('-------------------------')
        #print(expected_data)
        #print('--------------------------')
        self.assertEqual(serializer_data, expected_data)