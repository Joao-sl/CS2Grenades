# Generated by Django 5.1.5 on 2025-03-04 19:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs2grenades', '0013_alter_favorite_unique_together_alter_favorite_guide_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorite',
            name='unique_tutorial_favorite',
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'tutorial'), name='unique_tutorial_favorite'),
        ),
    ]
