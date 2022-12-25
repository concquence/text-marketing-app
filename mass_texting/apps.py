from django.apps import AppConfig


class MassTextingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mass_texting'

    def ready(self):
        import mass_texting.signals
