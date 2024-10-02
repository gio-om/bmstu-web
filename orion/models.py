from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Astronaut(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название", blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(default="images/default.png", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)

    space_time = models.IntegerField(blank=True)
    specialization = models.CharField(blank=True)
    country = models.CharField(blank=True)

    def get_image(self):
        return self.image.url.replace("minio", "localhost", 1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Астронавт"
        verbose_name_plural = "Астронавты"
        db_table = "astronauts"


class Flight(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершен'),
        (4, 'Отклонен'),
        (5, 'Удален')
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True,
                              related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Модератор", null=True,
                                  related_name='moderator')

    name = models.CharField(blank=True, null=True)
    goal = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "Полет №" + str(self.pk)

    def get_astronauts(self):
        return [
            setattr(item.astronaut, "value", item.value) or item.astronaut
            for item in AstronautFlight.objects.filter(flight=self)
        ]

    class Meta:
        verbose_name = "Полет"
        verbose_name_plural = "Полеты"
        ordering = ('-date_formation',)
        db_table = "flights"


class AstronautFlight(models.Model):
    astronaut = models.ForeignKey(Astronaut, models.DO_NOTHING, blank=True, null=True, unique=True)
    flight = models.ForeignKey(Flight, models.DO_NOTHING, blank=True, null=True, unique=True)
    value = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        verbose_name = "м-м"
        verbose_name_plural = "м-м"
        db_table = "astronaut_flight"
