# Generated by Django 5.0.6 on 2024-07-08 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_alter_message_body_alter_support_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='offer',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
