import hashlib


def get_image_hash(image_field):
    image_field.seek(0)
    hash_md5 = hashlib.md5()

    for chunk in image_field.chunks():
        hash_md5.update(chunk)

    image_field.seek(0)

    return hash_md5.hexdigest()


def image_changed(instance, field_name):
    from site_settings.models import SiteSettings
    if not instance.pk:
        return True

    original = SiteSettings.objects.get(pk=instance.pk)
    original_field = getattr(original, field_name)
    current_field = getattr(instance, field_name)

    return original_field.name != current_field.name
