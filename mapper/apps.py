from django.apps import AppConfig


class MapperConfig(AppConfig):
    name = 'mapper'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import mapper.signals.handlers