from django.conf import settings
from .apps import EjudgePlugConfig

class Router(object):
    def db_for_read(self, model, **hints):
        """"Point all read operations to the specific database."""
        if model._meta.app_label == EjudgePlugConfig.name:
            return settings.EJUDGE_PLUG_DB
        return None

    def db_for_write(self, model, **hints):
        """Point all write operations to the specific database."""
        if model._meta.app_label == EjudgePlugConfig.name:
            return settings.EJUDGE_PLUG_DB
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation between apps that use the same database."""
        db_obj1 = obj1._meta.app_label == settings.EJUDGE_PLUG_DB
        db_obj2 = obj2._meta.app_label == settings.EJUDGE_PLUG_DB
        if db_obj1 or db_obj2:
            return db_obj1 and db_obj2
        return None

    def allow_syncdb(self, db, model):
        """Make sure that apps only appear in the related database."""
        if db == settings.EJUDGE_PLUG_DB:
            return model._meta.app_label == EjudgePlugConfig.name
        elif model._meta.app_label == EjudgePlugConfig.name:
            return False
        return None
