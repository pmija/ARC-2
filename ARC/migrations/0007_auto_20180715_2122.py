# Generated by Django 2.0.6 on 2018-07-15 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARC', '0006_auto_20180715_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audittable_inventory',
            name='ItemID',
        ),
        migrations.AddField(
            model_name='audittable_inventory',
            name='ItemUniqueID',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inventory',
            name='ItemUniqueID',
            field=models.IntegerField(default=0),
        ),
    ]
