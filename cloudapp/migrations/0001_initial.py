# Generated by Django 4.2.1 on 2023-05-26 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicleId', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('owner', models.CharField(max_length=100)),
            ],
        ),
    ]