# Generated by Django 5.0.6 on 2024-07-08 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_chat_err'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='err',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
