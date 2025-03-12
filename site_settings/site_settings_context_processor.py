from site_settings.models import SiteSettings


def site_settings(request):
    data = SiteSettings.objects.first()
    return {
        'site_setting': data
    }
