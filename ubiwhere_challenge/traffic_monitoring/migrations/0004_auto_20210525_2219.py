# Generated by Django 3.2.3 on 2021-05-25 22:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traffic_monitoring', '0003_auto_20210525_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadspeed',
            name='caracterization',
            field=models.CharField(choices=[('H', 'High'), ('M', 'Moderate'), ('L', 'Low')], editable=False, max_length=9),
        ),
        migrations.AlterField(
            model_name='roadspeed',
            name='intensity',
            field=models.IntegerField(editable=False, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)]),
        ),
    ]