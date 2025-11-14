from django.core.management.base import BaseCommand
from dadjokes.models import Joke, Picture

class Command(BaseCommand):
    help = 'Seed the database with initial jokes and pictures'

    def handle(self, *args, **options):
        # Clear existing data
        Joke.objects.all().delete()
        Picture.objects.all().delete()
        
        # Add jokes
        jokes = [
            {
                'text': "Why don't scientists trust atoms? Because they make up everything!",
                'contributor': 'Dad'
            },
            {
                'text': "I invented a new word: Plagiarism!",
                'contributor': 'Dad'
            },
            {
                'text': "Why don't eggs tell jokes? They'd crack each other up!",
                'contributor': 'Dad'
            },
            {
                'text': "What do you call a fake noodle? An impasta!",
                'contributor': 'Dad'
            },
            {
                'text': "Why did the scarecrow win an award? He was outstanding in his field!",
                'contributor': 'Dad'
            },
            {
                'text': "I'm reading a book about anti-gravity. It's impossible to put down!",
                'contributor': 'Dad'
            },
            {
                'text': "What do you call a bear with no teeth? A gummy bear!",
                'contributor': 'Dad'
            },
            {
                'text': "Why did the coffee file a police report? It got mugged!",
                'contributor': 'Dad'
            }
        ]
        
        for joke_data in jokes:
            Joke.objects.create(**joke_data)
        
        # Add pictures with URLs (using actual funny GIFs and images)
        pictures = [
            {
                'image_url': 'https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif',
                'contributor': 'Dad'
            },
            {
                'image_url': 'https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif',
                'contributor': 'Dad'
            },
            {
                'image_url': 'https://media.giphy.com/media/mlvseq9yvZhba/giphy.gif',
                'contributor': 'Dad'
            },
            {
                'image_url': 'https://media.giphy.com/media/ICOgUNjpvO0PC/giphy.gif',
                'contributor': 'Dad'
            },
            {
                'image_url': 'https://media.giphy.com/media/mCRJDo24UvJMA/giphy.gif',
                'contributor': 'Dad'
            },
            {
                'image_url': 'https://media.giphy.com/media/MDJ9IbxxvDUQM/giphy.gif',
                'contributor': 'Dad'
            },
            {
                'image_url': 'https://media.giphy.com/media/cfuL5gqFDreXxkWQ4o/giphy.gif',
                'contributor': 'Dad'
            },
            {
                'image_url': 'https://media.giphy.com/media/l4FGGafcOHmrlQxG0/giphy.gif',
                'contributor': 'Dad'
            }
        ]
        
        for pic_data in pictures:
            Picture.objects.create(**pic_data)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully seeded database with {len(jokes)} jokes and {len(pictures)} pictures!')
        )
