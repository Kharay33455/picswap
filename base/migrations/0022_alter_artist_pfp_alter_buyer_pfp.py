# Generated by Django 5.0.6 on 2024-07-07 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_artist_pfp_buyer_pfp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='pfp',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='pfp',
            field=models.ImageField(blank=True, null=True, upload_to='images/pfp'),
        ),
    ]
