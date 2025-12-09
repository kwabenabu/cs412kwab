import csv
from django.core.management.base import BaseCommand
from project.models import CardSet
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Import card sets from cardsets_sample.csv'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'cardsets_sample.csv')
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                cardset, created = CardSet.objects.get_or_create(
                    name=row['name'],
                    brand=row['brand'],
                    release_year=row['release_year'],
                    defaults={
                        'sport': row['sport'],
                        'total_cards': row['total_cards'],
                        'description': row.get('description', ''),
                    }
                )
                if created:
                    count += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} card sets.'))
