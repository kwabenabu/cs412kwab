from django.core.management.base import BaseCommand
from dadjokes.models import Joke, Picture


class Command(BaseCommand):
    help = 'Seed the database with dad jokes and pictures'

    def handle(self, *args, **options):
        # Clear existing data
        Joke.objects.all().delete()
        Picture.objects.all().delete()

        # Add jokes
        jokes = [
            {"text": "Why don't scientists trust atoms? Because they make up everything!", "contributor": "Dad Bob"},
            {"text": "I told my wife she was drawing her eyebrows too high. She looked surprised.", "contributor": "Funny Frank"},
            {"text": "What do you call a fake noodle? An impasta!", "contributor": "Pasta Paul"},
            {"text": "Why don't eggs tell jokes? They'd crack each other up!", "contributor": "Egg Eric"},
            {"text": "I used to hate facial hair, but then it grew on me.", "contributor": "Beard Bill"},
            {"text": "What's the best thing about Switzerland? I don't know, but the flag is a big plus.", "contributor": "Swiss Sam"},
            {"text": "I only know 25 letters of the alphabet. I don't know Y.", "contributor": "Alpha Andy"},
            {"text": "Why did the scarecrow win an award? He was outstanding in his field!", "contributor": "Farm Fred"},
        ]

        for joke_data in jokes:
            Joke.objects.create(**joke_data)

        # Add pictures
        pictures = [
            {"image_url": "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif", "contributor": "Meme Mike"},
            {"image_url": "https://media.giphy.com/media/kPIswn0RfPTGxOvDj5/giphy.gif", "contributor": "Gif Gary"},
            {"image_url": "https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif", "contributor": "Funny Fred"},
            {"image_url": "https://media.giphy.com/media/26FLgGTPUDH6UGAbm/giphy.gif", "contributor": "LOL Larry"},
            {"image_url": "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif", "contributor": "Happy Hal"},
        ]

        for picture_data in pictures:
            Picture.objects.create(**picture_data)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(jokes)} jokes and {len(pictures)} pictures')
        )
