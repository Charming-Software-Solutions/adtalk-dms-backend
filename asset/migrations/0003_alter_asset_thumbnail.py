# Generated by Django 5.1.2 on 2024-10-27 17:08

import django.core.validators
import shared.validators
import storages.backends.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0002_asset_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3.S3Storage(), upload_to='asset_media', validators=[shared.validators.validate_image, django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])]),
        ),
    ]
