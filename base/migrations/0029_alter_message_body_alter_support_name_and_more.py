# Generated by Django 5.0.6 on 2024-07-08 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_chat_date_of_creation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='support',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='support_message',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]