# Generated by Django 2.0.6 on 2018-07-22 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARC', '0011_remove_inventory_uniqueid'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='QtyBorrowed',
            field=models.IntegerField(default=0),
        ),
    ]
