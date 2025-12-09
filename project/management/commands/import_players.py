import csv
from django.core.management.base import BaseCommand
from project.models import Player
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Import players from players_sample.csv'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'players_sample.csv')
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                player, created = Player.objects.get_or_create(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    defaults={
                        'birth_year': row['birth_year'],
                        'position': row['position'],
                        'club_team': row['club_team'],
                        'country': row['country'],
                        'image': row['image'] or None,
                    }
                )
                if created:
                    count += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} players.'))
