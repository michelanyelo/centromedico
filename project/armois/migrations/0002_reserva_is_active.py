# Generated by Django 5.0.1 on 2024-08-26 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armois', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
