# Generated by Django 2.0 on 2018-08-02 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARC', '0022_auto_20180802_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresidencyschedule',
            name='Schedule',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='studentresidencyschedule',
            name='Student',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='NFCUniqueID',
            field=models.CharField(default='', max_length=250),
        ),
    ]
