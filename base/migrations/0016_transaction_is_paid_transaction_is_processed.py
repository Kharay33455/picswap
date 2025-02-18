# Generated by Django 5.0.6 on 2024-07-06 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_transaction_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
    ]
