from django.apps import AppConfig


class VendormisConfig(AppConfig):
    name = 'vendormis'

    def ready(self):
        import vendormis.signals
