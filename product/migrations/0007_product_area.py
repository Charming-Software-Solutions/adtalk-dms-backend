# Generated by Django 5.1.3 on 2024-11-21 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_product_expiration'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='area',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
