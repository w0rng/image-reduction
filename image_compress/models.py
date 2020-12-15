from django.db import models
from django.contrib.postgres.fields import ArrayField 
from server.settings import CODE_SIZE

class Data(models.Model):
    array = ArrayField(
            models.IntegerField(),
            size=CODE_SIZE,
            verbose_name='Закодированное изображение'
        )