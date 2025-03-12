# Generated by Django 5.1.5 on 2025-02-18 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs2grenades', '0004_tags_alter_activemappool_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guideposts',
            name='slug',
            field=models.SlugField(help_text='Auto-populated, this will be the URL for the post', unique=True),
        ),
        migrations.AlterField(
            model_name='tags',
            name='help_text',
            field=models.TextField(default='You can add these tags to the posts', editable=False),
        ),
    ]
