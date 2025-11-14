from django.core.management.base import BaseCommand
from dadjokes.models import Joke, Picture

JOKES = [
    ("Why did the scarecrow win an award? Because he was outstanding in his field.", "Alex"),
    ("I would tell you a construction joke, but I'm still working on it.", "Sam"),
    ("Why don't eggs tell jokes? They'd crack each other up.", "Jordan"),
    ("I used to hate facial hair... but then it grew on me.", "Casey"),
    ("What do you call cheese that isn't yours? Nacho cheese.", "Taylor"),
]

PICTURES = [
    ("https://placekitten.com/400/300", "Mia"),
    ("https://placebear.com/400/300", "Riley"),
    ("https://picsum.photos/seed/fun/400/300", "Jamie"),
    ("https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif", "Avery"),
    ("https://media.giphy.com/media/l0HlymVw5VOxsZomI/giphy.gif", "Quinn"),
]


class Command(BaseCommand):
    help = "Seed the database with G-rated dad jokes and pictures"

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true',
                            help='Delete all existing jokes and pictures before seeding')

    def handle(self, *args, **options):
        reset = options.get('reset')
        if reset:
            self.stdout.write("Resetting dadjokes data...")
            Joke.objects.all().delete()
            Picture.objects.all().delete()

        created_jokes = 0
        for text, who in JOKES:
            _, created = Joke.objects.get_or_create(text=text, defaults={'contributor': who})
            if created:
                created_jokes += 1

        created_pics = 0
        for url, who in PICTURES:
            _, created = Picture.objects.get_or_create(image_url=url, defaults={'contributor': who})
            if created:
                created_pics += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Jokes created: {created_jokes}, Pictures created: {created_pics}."
        ))
