from django.apps import AppConfig


class PublisherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'publisher'

    def ready(self):
        import publisher.singals
