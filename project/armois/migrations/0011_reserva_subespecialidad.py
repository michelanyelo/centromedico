# Generated by Django 5.0.1 on 2024-08-25 17:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armois', '0010_alter_reserva_especialidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='subespecialidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='armois.subespecialidad'),
        ),
    ]