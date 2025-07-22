from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Application'

    def ready(self):
        from .signals import initial_data
        post_migrate.connect(initial_data, sender=self)
