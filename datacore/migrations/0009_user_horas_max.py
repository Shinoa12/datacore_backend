# Generated by Django 5.0.5 on 2024-06-24 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacore', '0008_ajustes'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='horas_max',
            field=models.PositiveIntegerField(default=1),
        ),
    ]