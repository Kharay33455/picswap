# Generated by Django 5.0.6 on 2024-07-06 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_rename_itmes_transaction_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
