# Generated by Django 2.0 on 2018-07-29 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARC', '0017_auto_20180729_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='audittable_inventory',
            name='Event',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='audittable_inventory',
            name='Remarks',
            field=models.CharField(default='', max_length=250),
        ),
    ]
