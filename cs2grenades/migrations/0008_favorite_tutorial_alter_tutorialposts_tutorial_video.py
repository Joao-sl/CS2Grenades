# Generated by Django 5.1.5 on 2025-03-03 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs2grenades', '0007_alter_guideposts_options_tutorialposts'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='tutorial',
            field=models.ForeignKey(default=4324, on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='cs2grenades.tutorialposts'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tutorialposts',
            name='tutorial_video',
            field=models.TextField(),
        ),
    ]
