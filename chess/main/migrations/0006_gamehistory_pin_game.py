# Generated by Django 4.2 on 2023-06-06 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_gamehistory_username_b_gamehistory_username_w'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamehistory',
            name='pin_game',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
