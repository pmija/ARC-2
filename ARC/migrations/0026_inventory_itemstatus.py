# Generated by Django 2.0 on 2018-08-07 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARC', '0025_auto_20180805_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='ItemStatus',
            field=models.IntegerField(default=1),
        ),
    ]
