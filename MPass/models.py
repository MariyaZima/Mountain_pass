from django.db import models


class Mountain(models.Model):
    CHOICE_STATUS = (
        ("new", 'новый'),
        ("pending", 'модератор взял в работу'),
        ("accepted", 'модерация прошла успешно'),
        ("rejected", 'модерация прошла, информация не принята'),
    )

    beauty_title = models.CharField(max_length=255, verbose_name='Название препятствий')
    title = models.CharField(max_length=255, verbose_name='Название вершины')
    other_titles = models.CharField(max_length=255, verbose_name='Другое название')
    connect = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=CHOICE_STATUS, default="new")
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='users')
    coord = models.ForeignKey('Coords', on_delete=models.CASCADE, related_name='coords')
    level = models.ForeignKey('Level', on_delete=models.CASCADE, related_name='level')

    class Meta:
        verbose_name = 'Перевал'
        verbose_name_plural = 'Перевалы'

    def __str__(self):
        return f'{self.pk}, {self.beauty_title}'


class User(models.Model):
    email = models.EmailField()
    fam = models.CharField(max_length=255, verbose_name='Фамилия')
    name = models.CharField(max_length=255, verbose_name='Имя')
    otc = models.CharField(max_length=255, verbose_name='Отчество')
    phone = models.CharField(max_length=255, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'имя: {self.name}, фамилия: {self.fam}, отчество: {self.otc}'


class Coords(models.Model):
    latitude = models.FloatField(max_length=30, verbose_name='Широта', blank=True, null=True)
    longitude = models.FloatField(max_length=30, verbose_name='Долгота', blank=True, null=True)
    height = models.IntegerField(verbose_name='Высота', blank=True, null=True)

    def __str__(self):
        return f'широта: {self.latitude}, долгота: {self.longitude}, высота: {self.height}'

    class Meta:
        verbose_name = 'Координаты'
        verbose_name_plural = 'Координаты'


class Level(models.Model):
    CHOICE_LEVEL = (
        ('1A', '1A'),
        ('2A', '2A'),
        ('3A', '3A'),
        ('4A', '4A'),
    )

    winter = models.CharField(max_length=4, choices=CHOICE_LEVEL, verbose_name='Зима', default="1A")
    summer = models.CharField(max_length=4, choices=CHOICE_LEVEL, verbose_name='Лето', default="1A")
    autumn = models.CharField(max_length=4, choices=CHOICE_LEVEL, verbose_name='Осень', default="1A")
    spring = models.CharField(max_length=4, choices=CHOICE_LEVEL, verbose_name='Весна', default="1A")

    def __str__(self):
        return f'зима: {self.winter}, лето: {self.summer}, осень: {self.autumn}, осень: {self.spring}'

    class Meta:
        verbose_name = 'Уровень сложности'
        verbose_name_plural = 'Уровни сложности'


class Images(models.Model):
    data = models.ImageField(upload_to="images", verbose_name='Фото перевала', blank=True)
    title = models.CharField(max_length=124, verbose_name='Название фото')
    mountain_id = models.ForeignKey(Mountain, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'{self.pk}: {self.title}'