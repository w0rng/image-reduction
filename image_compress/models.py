from django.db import models
from django.contrib.postgres.fields import ArrayField 
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from server.settings import CODE_SIZE
import PIL
import numpy as np
from . import views
import datetime
import os
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Почта', unique=True)
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)

    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


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
    name = models.CharField('Название', max_length=255, editable = False)
    data = models.ForeignKey(Data, models.CASCADE, verbose_name='Данные', null=True, blank=True, editable = False)
    date = models.DateField('Дата загрузки', default=datetime.date.today, editable = False)
    size = models.IntegerField('Размер изображения', editable = False)
    obj = models.ForeignKey(Object, models.CASCADE, verbose_name='Объект', blank=True, null=True, editable = False)
    img = models.ImageField('Изображение', null=True, blank=True)
    user = models.ForeignKey(User, models.CASCADE, null=True, blank=True, editable = False, verbose_name='Пользователь')

    def save(self, *args, **kwargs):
        im = PIL.Image.open(self.img)
        self.size = im._size[0] * im._size[1] * 3
        self.name = self.img.name
        im.convert('RGB')
        im.thumbnail((32, 32))
        im = np.array(im.getdata()).reshape((32, 32, 3))
        predictions = views.predict(im[None])
        type_ = np.argmax(predictions, axis=1)[0] + 1
        self.obj = Object.objects.filter(id=type_).first()
        code = list(views.encoder(im[None])[0])
        code = list(map(int, code))

        d = Data(array=code)
        d.save()
        self.data = d

        super().save(*args, **kwargs)

        os.remove(self.img.name)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.name
