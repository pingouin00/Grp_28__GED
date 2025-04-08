from django.apps import AppConfig

class DocumentManagementConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'Document_Management'
