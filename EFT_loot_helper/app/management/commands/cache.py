from typing import Any
from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.core.management.base import CommandParser

class Command(BaseCommand):
    help = "This command uses for operating with cache."

    def add_arguments(self, parser: CommandParser) -> None:
        
        parser.add_argument(
            "-c",
            "--clear",
            action="store_true",
            default=False,
            help="Use this argument to clear the cache.",
        )

        parser.add_argument(
            "-C",
            "--check",
            nargs='+',
            type=str,
            action='store',
            default=False,
            help="Use this argument to check, if the object exists in the cache.",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        if options['clear']:
            cache.clear()
            self.stdout.write(
                self.style.SUCCESS("Cache cleaned successfully.")
            )
        elif options['check']:
            if cache.has_key(options['check'][0]):
                self.stdout.write(
                    self.style.SUCCESS(f"The cache has the key '{options['check'][0]}'")
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f"The cache does not have the key '{options['check'][0]}'")
                )