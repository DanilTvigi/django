# Generated by Django 4.2 on 2023-05-18 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_sessionconnection_user2'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionconnection',
            name='type_game',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
