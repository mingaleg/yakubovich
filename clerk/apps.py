from django.apps import AppConfig


class ClerkConfig(AppConfig):
    name = 'clerk'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import clerk.signals.handlers

