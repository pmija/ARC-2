# Generated by Django 2.0.6 on 2018-07-11 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARC', '0002_auto_20180704_0609'),
    ]

    operations = [
        migrations.AddField(
            model_name='audittable_inventory',
            name='BorrowStatus',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='audittable_inventory',
            name='Borrower',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='audittable_inventory',
            name='Lender',
            field=models.IntegerField(null=True),
        ),
    ]