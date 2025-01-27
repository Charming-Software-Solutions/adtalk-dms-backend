# Generated by Django 5.1.2 on 2024-10-26 04:04

import django.core.validators
import django.db.models.deletion
import shared.validators
import storages.backends.s3
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(help_text='Unique identifier for the item', max_length=50, unique=True)),
                ('condition', models.CharField(choices=[('NEW', 'New'), ('GOOD', 'Good'), ('FAIR', 'Fair'), ('POOR', 'Poor'), ('DAMAGED', 'Damaged')], default='GOOD', max_length=20)),
                ('status', models.CharField(choices=[('AVAILABLE', 'Available'), ('IN_USE', 'In Use'), ('MAINTENANCE', 'Under Maintenance'), ('LOST', 'Lost')], default='AVAILABLE', max_length=20)),
                ('thumbnail', models.ImageField(blank=True, null=True, storage=storages.backends.s3.S3Storage(), upload_to='asset_images', validators=[shared.validators.validate_image, django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])])),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.assettype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
