# Generated by Django 5.0.6 on 2024-07-07 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_artist_has_new_message_buyer_has_new_message_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='chat_id',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
