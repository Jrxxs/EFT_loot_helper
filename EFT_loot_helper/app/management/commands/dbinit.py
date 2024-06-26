from typing import Any
from ...models import CachedItem
from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.core.management.base import CommandParser


class Command(BaseCommand):
    help = "This command initializes the DataBase from the cache."

    def add_arguments(self, parser: CommandParser) -> None:
        
        parser.add_argument(
            "-I",
            "--items",
            action="store_true",
            help="This argument is used to initialize items."
        )


    def handle(self, *args: Any, **options: Any) -> str | None:
        if options["items"]:
            items = cache.get("items")
            if items is None:
                self.stdout.write(
                    self.style.ERROR("Cache has no items.")
                )
                return

            for i in items:
                CachedItem.objects.update_or_create(name=i["name"], itemId=i["id"])
            else:
                self.stdout.write(
                    self.style.SUCCESS("The items table has been initialized.")
                )
        else:
            self.stdout.write(
                self.style.ERROR("Unknown command.")
            )