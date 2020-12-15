# Generated by Django 3.1.4 on 2020-12-15 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image_compress', '0002_auto_20201215_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('date', models.DateField(verbose_name='Дата загрузки')),
                ('size', models.IntegerField(verbose_name='Размер изображения')),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image_compress.data', verbose_name='Данные')),
                ('obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='image_compress.object', verbose_name='Объект')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
    ]