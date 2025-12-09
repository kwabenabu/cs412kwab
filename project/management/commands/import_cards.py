import csv
from django.core.management.base import BaseCommand
from project.models import Card, Player, CardSet
from django.conf import settings
import os
from django.utils.dateparse import parse_date

class Command(BaseCommand):
    help = 'Import cards from cards_sample.csv'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'cards_sample.csv')
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                try:
                    player = Player.objects.get(first_name=row['player_first_name'], last_name=row['player_last_name'])
                    cardset = CardSet.objects.get(name=row['set_name'])
                except (Player.DoesNotExist, CardSet.DoesNotExist):
                    self.stdout.write(self.style.WARNING(f"Skipping card: player or set not found for {row}"))
                    continue
                card, created = Card.objects.get_or_create(
                    player=player,
                    set=cardset,
                    card_number=row['card_number'],
                    defaults={
                        'rarity': row['rarity'],
                        'serial_number': row['serial_number'] or None,
                        'image': row['image'] or None,
                        'estimated_value': row['estimated_value'] or 0,
                        'is_numbered': row['is_numbered'].upper() == 'TRUE',
                        'created_at': parse_date(row['created_at']) if row['created_at'] else None,
                    }
                )
                if created:
                    count += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} cards.'))
