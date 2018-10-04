# Generated by Django 2.0 on 2018-08-01 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ARC', '0019_ref_laboratory_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='residencytimeslot',
            name='Term',
        ),
        migrations.RemoveField(
            model_name='studentresidencyschedule',
            name='Group',
        ),
        migrations.AddField(
            model_name='residencytimeslot',
            name='TakenSlot',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='residencytimeslot',
            name='TotalSlot',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentresidencyschedule',
            name='Schedule',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='studentresidencyschedule',
            name='Student',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='residencytimeslot',
            name='Laboratory',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='ARC.Ref_Laboratory'),
        ),
        migrations.AlterField(
            model_name='residencytimeslot',
            name='Schedule',
            field=models.CharField(default='', max_length=50),
        ),
    ]
