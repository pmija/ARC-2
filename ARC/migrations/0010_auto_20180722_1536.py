# Generated by Django 2.0.6 on 2018-07-22 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ARC', '0009_auto_20180722_1533'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audittable_inventory',
            old_name='ItemUniqueID',
            new_name='ItemID',
        ),
    ]