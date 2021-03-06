# Generated by Django 3.1.4 on 2021-01-11 22:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='photo',
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.BigIntegerField(default=61737373, validators=[django.core.validators.MinValueValidator(61000000), django.core.validators.MaxValueValidator(65999999)], verbose_name='phone_number'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=250, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(choices=[('Ag', 'Ashgabat'), ('Bl', 'Balkan'), ('Mr', 'Mary'), ('Dz', 'Dasoguz'), ('Lb', 'Lebap')], max_length=2, verbose_name='city'),
        ),
    ]
