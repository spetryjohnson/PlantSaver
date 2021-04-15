# Generated by Django 3.1.7 on 2021-04-13 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='SoilSensor',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('ANALOG', 'Analog'), ('I2C', 'I2C')], max_length=10)),
                ('i2cAddr', models.CharField(max_length=5, null=True)),
                ('analogInputNumber', models.IntegerField(null=True)),
                ('assignedToPlant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='plantWatering.plant')),
            ],
        ),
        migrations.CreateModel(
            name='Pump',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('12V', '12V')], max_length=10)),
                ('zoneNumberOnHAT', models.IntegerField()),
                ('assignedToPlant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='plantWatering.plant')),
            ],
        ),
    ]
