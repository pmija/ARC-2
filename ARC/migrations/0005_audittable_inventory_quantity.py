# Generated by Django 2.0.6 on 2018-07-11 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARC', '0004_auto_20180711_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='audittable_inventory',
            name='Quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
