from django.contrib import admin
from django.http import HttpRequest
from site_settings.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = 'id', 'site_name', 'email'
    list_display_links = 'id', 'site_name', 'email'

    # There can be only one SiteSettings
    def has_add_permission(self, request):
        if not SiteSettings.objects.exists():
            return True
