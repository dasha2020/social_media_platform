from django.apps import AppConfig


class SocialMediaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_media_app'

    def ready(self):
        import social_media_app.signals
