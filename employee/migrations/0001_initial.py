# Generated by Django 5.1.2 on 2024-11-14 08:31

import django.core.validators
import django.db.models.deletion
import shared.validators
import storages.backends.s3
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('profile_image', models.ImageField(blank=True, null=True, storage=storages.backends.s3.S3Storage(), upload_to='employee_media', validators=[shared.validators.validate_image, django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]