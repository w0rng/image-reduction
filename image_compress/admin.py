from django.contrib import admin
from . import models

@admin.register(models.Data)
class Data(admin.ModelAdmin):
    list_display = ('id', 'array')


@admin.register(models.Object)
class Object(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.User)
class User(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')


@admin.register(models.Image)
class Image(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'size', 'obj', 'user')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()