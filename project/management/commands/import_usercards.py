import csv
from django.core.management.base import BaseCommand
from project.models import UserCard, Card
from django.contrib.auth import get_user_model
from django.conf import settings
import os
from django.utils.dateparse import parse_date

class Command(BaseCommand):
    help = 'Import user cards from usercards_sample.csv'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'usercards_sample.csv')
        User = get_user_model()
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                try:
                    user = User.objects.get(username=row['user'])
                    card = Card.objects.get(pk=row['card'])
                except (User.DoesNotExist, Card.DoesNotExist):
                    self.stdout.write(self.style.WARNING(f"Skipping usercard: user or card not found for {row}"))
                    continue
                usercard, created = UserCard.objects.get_or_create(
                    user=user,
                    card=card,
                    defaults={
                        'purchase_price': row['purchase_price'] or 0,
                        'purchase_date': parse_date(row['purchase_date']) if row['purchase_date'] else None,
                        'grade': row['grade'],
                        'grade_score': row['grade_score'] or None,
                        'condition_note': row['condition_note'],
                        'for_sale': row['for_sale'].upper() == 'TRUE',
                        'sale_price': row['sale_price'] or None,
                    }
                )
                if created:
                    count += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} user cards.'))
