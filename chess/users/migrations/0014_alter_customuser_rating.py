# Generated by Django 4.2 on 2023-06-14 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_sessionconnection_cords_ancle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='rating',
            field=models.FloatField(default=0, null=True),
        ),
    ]