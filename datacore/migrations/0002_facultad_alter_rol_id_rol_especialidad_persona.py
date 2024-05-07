# Generated by Django 5.0.4 on 2024-05-07 06:31

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facultad',
            fields=[
                ('id_facultad', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='rol',
            name='id_rol',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id_especialidad', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('id_facultad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datacore.facultad')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id_persona', models.IntegerField(primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=200)),
                ('apellidos', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('authorize_flag', models.BooleanField(default=False)),
                ('motivo', models.CharField(max_length=500)),
                ('fecha_registro', models.DateTimeField(default=datetime.date.today)),
                ('recursos_max', models.IntegerField(default=1)),
                ('id_especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datacore.especialidad')),
                ('id_facultad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datacore.facultad')),
                ('id_rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datacore.rol')),
            ],
        ),
    ]
