# Generated by Django 3.1.2 on 2020-12-08 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20201207_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlisted',
            name='trueOrFalse',
            field=models.BooleanField(default=False),
        ),
    ]
