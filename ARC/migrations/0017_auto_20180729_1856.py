# Generated by Django 2.0 on 2018-07-29 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ARC', '0016_auto_20180729_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audittable_inventory',
            name='Admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_users', to='ARC.User'),
        ),
        migrations.AlterField(
            model_name='audittable_inventory',
            name='Borrower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='borrower_users', to='ARC.User'),
        ),
        migrations.AlterField(
            model_name='audittable_inventory',
            name='ItemID',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='ARC.Inventory'),
        ),
    ]