from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'apps.documents'
    verbose_name = 'Documents'
