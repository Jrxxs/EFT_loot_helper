from django.apps import AppConfig
from django.core.management.commands import runserver
from django.core.cache import cache
from .tasks import periodic_eft_api_query
import sys

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    # что-то может не завестись.
    # возможно стоит переписать на другой конфиг без этих команд
    other_commands = [
        'cache',
        'makemigrations',
        'migrate',
    ]

    def ready(self) -> None:
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        
        query_schedule, _ = IntervalSchedule.objects.get_or_create(
            every=5,
            period=IntervalSchedule.MINUTES,
        )

        PeriodicTask.objects.get_or_create(
            interval=query_schedule,
            name="Periodic query to tarkov.api",
            task='app.tasks.periodic_eft_api_query'
        )

        if not cache.has_key("items"):
            for i in self.other_commands:
                if i not in sys.argv:
                    continue
                else:
                    break
            else:
                periodic_eft_api_query()

        # schedule_getter, _ = IntervalSchedule.objects.get_or_create(
        #     every=2,
        #     period=IntervalSchedule.SECONDS,
        # )

        # PeriodicTask.objects.get_or_create(
        #     interval=schedule_getter,
        #     name="Test periodic task getter",
        #     task='app.tasks.my_periodic_task_getter'
        # )
