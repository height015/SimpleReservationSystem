# Generated by Django 3.1.2 on 2021-12-31 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_auto_20211231_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='available',
            name='Available_count',
            field=models.IntegerField(max_length=255),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='NumSeats_reserved',
            field=models.IntegerField(max_length=255),
        ),
    ]
