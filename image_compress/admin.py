from django.contrib import admin
from . import models

@admin.register(models.Data)
class Data(admin.ModelAdmin):
    list_display = ('id', 'array')


@admin.register(models.Object)
class Object(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.Image)
class Image(admin.ModelAdmin):
    list_display = ('id', 'name', 'data', 'date', 'size', 'obj')
