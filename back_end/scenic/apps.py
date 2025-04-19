from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class ScenicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scenic'

    # def ready(self):
    #     from scenic.task import auto_check_thread
    #     auto_check_thread.start()
