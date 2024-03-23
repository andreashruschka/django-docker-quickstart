from django.core.management.base import BaseCommand
from ...models import Post, Comment
import requests


class Command(BaseCommand):
    help = "Gets and saves posts from https://jsonplaceholder.typicode.com"

    def add_arguments(self, parser):
        parser.add_argument("--is_test", action='store_true', help="Run in test mode (data will not be saved in "
                                                                   "database)")

    def handle(self, *args, **options):
        api_url = 'https://jsonplaceholder.typicode.com/posts'
        is_test = options.get('is_test', True)
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            if is_test:
                self.stdout.write(
                    self.style.SUCCESS(
                        "{} Posts successfully fetched during testing, no data saved in db".format(len(data))))
            else:
                saved_posts = 0
                for item in data:
                    Post.objects.create(
                        userId=item["userId"],
                        pk=item["id"],
                        title=item["title"],
                        body=item["body"],
                    )
                    saved_posts = saved_posts + 1
                self.stdout.write(self.style.SUCCESS("{} Posts successfully fetch and saved".format(saved_posts)))
        except requests.RequestException as e:
            self.stdout.write(self.style.Error("Error fetching Post objects: {} ".format(e)))
