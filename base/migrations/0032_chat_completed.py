# Generated by Django 5.0.6 on 2024-07-08 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_swap_artist_available_balance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
