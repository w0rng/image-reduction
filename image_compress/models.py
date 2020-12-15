from django.db import models
from django.contrib.postgres.fields import ArrayField 
from server.settings import CODE_SIZE

class Data(models.Model):
    array = ArrayField(
            models.IntegerField(),
            size=CODE_SIZE,
            verbose_name='Данные'
        )
    
    class Meta:
        verbose_name = 'Закодированное изображение'
        verbose_name_plural = 'Закодированные изображения'


class Object(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return self.name