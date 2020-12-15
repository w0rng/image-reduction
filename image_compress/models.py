from django.db import models
from django.contrib.postgres.fields import ArrayField, array 
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

    def __str__(self):
        return f'{self.array[:5]}...{self.array[-5:]}'.replace('[', '').replace(']', '')

class Object(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField('Название', max_length=255)
    data = models.ForeignKey(Data, models.CASCADE, verbose_name='Данные')
    date = models.DateField('Дата загрузки')
    size = models.IntegerField('Размер изображения')
    obj = models.ForeignKey(Object, models.CASCADE, verbose_name='Объект', blank=True, null=True)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.name
