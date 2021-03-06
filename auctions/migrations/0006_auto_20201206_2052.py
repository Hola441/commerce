# Generated by Django 3.1.2 on 2020-12-07 02:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20201206_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='number_of_bids',
        ),
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.IntegerField(auto_created=True, default=0),
        ),
        migrations.AlterField(
            model_name='listing',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
