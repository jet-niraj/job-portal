from django.apps import AppConfig


class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'
    verbose_name = 'Job Management System'
    
    def ready(self):
        """
        Signal handlers can be registered here if needed
        """
        pass