# Generated by Django 4.2 on 2023-05-20 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_sessionconnection_type_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionconnection',
            name='expiry_time',
            field=models.PositiveIntegerField(default=60),
        ),
    ]
