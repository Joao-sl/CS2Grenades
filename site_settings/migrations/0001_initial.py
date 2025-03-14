# Generated by Django 5.1.5 on 2025-02-14 18:07

import cs2grenades.utils.images
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(
                    blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=254, null=True)),
                ('youtube', models.URLField(blank=True, null=True)),
                ('tiktok', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo/%Y/%m',
                 validators=[cs2grenades.utils.images.validate_image_size])),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='favicon/%Y/%m',
                 validators=[cs2grenades.utils.images.validate_image_dimensions])),
            ],
        ),
    ]
