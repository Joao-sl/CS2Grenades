from typing import Iterable
from django.db import models
from cs2grenades.utils.images import validate_image_size, validate_image_dimensions, resize_image
from site_settings.utils.images import image_changed
from django_cleanup import cleanup


@cleanup.select
class SiteSettings(models.Model):
    verbose_name = 'Site Settings'
    verbose_name_plural = 'Site Settings'

    site_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)

    youtube = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    logo = models.ImageField(
        upload_to='logo/%Y/%m',
        validators=[validate_image_size],
        blank=True,
        null=True
    )
    favicon = models.ImageField(
        upload_to='favicon/%Y/%m',
        validators=[validate_image_dimensions],
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if self.favicon and self.favicon.name:
            if image_changed(self, 'favicon'):
                self.favicon = resize_image(self.favicon, width=32, height=32)

        return super().save()

    def __str__(self):
        return self.site_name
