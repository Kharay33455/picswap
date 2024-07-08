# Generated by Django 5.0.6 on 2024-07-08 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_chat_is_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='is_read',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='is_read',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='is_read',
        ),
        migrations.AddField(
            model_name='chat',
            name='read_by_artist',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chat',
            name='read_by_buyer',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
