# Generated by Django 5.1.7 on 2025-05-09 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiscal_year', '0002_remove_fiscalyear_end_date_eng_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fiscalyear',
            name='is_active',
        ),
        migrations.AddField(
            model_name='fiscalyear',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active'),
        ),
    ]
