# Generated by Django 5.0.6 on 2024-07-07 17:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_remove_chat_body_remove_chat_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='piece',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.images'),
            preserve_default=False,
        ),
    ]
