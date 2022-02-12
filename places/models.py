from django.db import models
from django.utils import timezone


class Place(models.Model):
    address = models.CharField(
        "адрес",
        max_length=100,
        unique=True,
        db_index=True,
    )
    lat = models.FloatField(
        "широта",
        null=True,
        blank=True,
    )
    lon = models.FloatField(
        "долгота",
        null=True,
        blank=True,
    )
    request_time = models.DateTimeField(
        "время запроса",
        default=timezone.now,
        db_index=True,
    )

    class Meta:
        verbose_name = "геопозиция места"
        verbose_name_plural = "геопозиции мест"

    def __str__(self):
        return self.address
