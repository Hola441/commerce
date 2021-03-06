# Generated by Django 3.1.2 on 2020-12-07 01:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20201206_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='users',
            field=models.ManyToManyField(blank='True', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(max_length=64),
        ),
    ]
