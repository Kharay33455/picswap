# Generated by Django 5.0.6 on 2024-07-05 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_copyright'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copyright',
            name='co_authors',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]