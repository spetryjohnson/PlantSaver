# Generated by Django 3.1.7 on 2021-04-15 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plantWatering', '0009_wateringlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wateringlog',
            name='sensor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plantWatering.soilsensor'),
        ),
    ]
