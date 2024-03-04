from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Gets and saves posts and comments from https://jsonplaceholder.typicode.com"

    def add_arguments(self, parser):
        parser.add_argument("is_test", type=bool)

    def handle(self, *args, **options):
        print("TODO")
