# Generated by Django 4.2.1 on 2023-06-01 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloudapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicles',
            old_name='name',
            new_name='organization',
        ),
        migrations.RemoveField(
            model_name='vehicles',
            name='owner',
        ),
    ]