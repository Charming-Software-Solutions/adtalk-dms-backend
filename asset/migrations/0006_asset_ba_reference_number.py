# Generated by Django 5.1.3 on 2024-11-21 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0005_asset_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='ba_reference_number',
            field=models.CharField(blank=True, help_text='Reference number for logistics', max_length=100, null=True),
        ),
    ]
