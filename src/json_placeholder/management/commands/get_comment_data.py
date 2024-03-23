from django.core.management.base import BaseCommand
from ...models import Comment
import requests


class Command(BaseCommand):
    help = "Gets and saves comments from https://jsonplaceholder.typicode.com"

    def add_arguments(self, parser):
        parser.add_argument("--is_test", action='store_true', help="Run in test mode (data will not be saved in "
                                                                   "database)")

    def handle(self, *args, **options):
        api_url = 'https://jsonplaceholder.typicode.com/comments'
        is_test = options.get('is_test', True)
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            if is_test:
                self.stdout.write(
                    self.style.SUCCESS("{} Comments successfully fetched during testing, no data saved in db".format(len(data))))
            else:
                saved_comments = 0
                for item in data:
                    Comment.objects.create(
                        postId_id=item["postId"],
                        name=item["name"],
                        email=item["email"],
                        body=item["body"],
                    )
                    saved_comments = saved_comments + 1
                self.stdout.write(self.style.SUCCESS("{} Comments successfully fetch and saved".format(saved_comments)))
        except requests.RequestException as e:
            self.stdout.write(self.style.Error("Error fetching Post objects: {} ".format(e)))

