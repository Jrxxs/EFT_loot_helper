import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EFT_loot_helper.settings")
application = Celery("EFT_loot_helper")
application.config_from_object("django.conf:settings", namespace="CELERY")
application.autodiscover_tasks()


# @application.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')