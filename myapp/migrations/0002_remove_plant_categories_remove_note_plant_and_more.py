# Generated by Django 5.0.6 on 2024-08-16 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='note',
            name='plant',
        ),
        migrations.RemoveField(
            model_name='plant',
            name='species',
        ),
        migrations.RemoveField(
            model_name='plant',
            name='user',
        ),
        migrations.RemoveField(
            model_name='wateringschedule',
            name='plant',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Note',
        ),
        migrations.DeleteModel(
            name='Species',
        ),
        migrations.DeleteModel(
            name='Plant',
        ),
        migrations.DeleteModel(
            name='WateringSchedule',
        ),
    ]
