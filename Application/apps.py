from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Application'

    def ready(self):
        import Application.signals
