from django.apps import AppConfig


class Cs2GrenadesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cs2grenades'

    def ready(self):
        import cs2grenades.signals
