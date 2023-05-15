from django.apps import AppConfig


class ClassBasedConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "class_based"
