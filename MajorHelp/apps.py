from django.apps import AppConfig


class MajorhelpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MajorHelp'

    # clears all reviews on every server start
    def ready(self):
        from MajorHelp.models import MajorReview
        MajorReview.objects.all().delete()
