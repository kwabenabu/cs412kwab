from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from project.models import Player, CardSet, Card, UserCard
from datetime import date
from decimal import Decimal

class Command(BaseCommand):
    help = 'Load initial data for soccer trading card portfolio'

    def handle(self, *args, **options):
        # Clear existing data
        UserCard.objects.all().delete()
        Card.objects.all().delete()
        CardSet.objects.all().delete()
        Player.objects.all().delete()
        
        # Create Players
        players = [
            {
                'first_name': 'Lionel',
                'last_name': 'Messi',
                'country': 'Argentina',
                'position': 'RW',
                'club_team': 'Inter Miami',
                'birth_year': 1987,
                'image': 'https://assets.goal.com/v3/assets/bltcc7a7ffd2fbf71f5/blt3d8c7c9bc1dc7622/60db5444036e5c0fb5ac2ce5/80e060c69773b131bc0128e87bc642e0.jpg'
            },
            {
                'first_name': 'Cristiano',
                'last_name': 'Ronaldo',
                'country': 'Portugal',
                'position': 'ST',
                'club_team': 'Al Nassr',
                'birth_year': 1985,
                'image': 'https://assets.goal.com/v3/assets/bltcc7a7ffd2fbf71f5/bltbb10d3ec9eb7dddd/63ec5e2c0238a5003de734e4/GettyImages-1246313947.jpg'
            },
            {
                'first_name': 'Kylian',
                'last_name': 'Mbappe',
                'country': 'France',
                'position': 'ST',
                'club_team': 'Real Madrid',
                'birth_year': 1998,
                'image': 'https://assets.goal.com/v3/assets/bltcc7a7ffd2fbf71f5/bltadb67737000b6800/6481da01d71a0b2a24b88679/Kylian_Mbappe_PSG_2022-23.jpg'
            },
            {
                'first_name': 'Erling',
                'last_name': 'Haaland',
                'country': 'Norway',
                'position': 'ST',
                'club_team': 'Manchester City',
                'birth_year': 2000,
                'image': 'https://assets.goal.com/v3/assets/bltcc7a7ffd2fbf71f5/blt1073df19e0821a5b/64f780ccba2d361b6a884a7b/Erling_Haaland_Manchester_City_2023-24_PowerRankings_(27).jpg'
            },
            {
                'first_name': 'Kevin',
                'last_name': 'De Bruyne',
                'country': 'Belgium',
                'position': 'CAM',
                'club_team': 'Manchester City',
                'birth_year': 1991,
                'image': 'https://assets.goal.com/v3/assets/bltcc7a7ffd2fbf71f5/blt06a952fe34a45420/633f11109aad0e001c5014a5/Kevin_De_Bruyne_Manchester_City_2022-23.jpg'
            }
        ]

        for player_data in players:
            player = Player.objects.create(**player_data)
            self.stdout.write(f'Created player: {player}')

        # Create Card Sets
        card_sets = [
            {
                'name': 'Prizm Premier League',
                'brand': 'PANINI',
                'release_year': 2023,
                'sport': 'Soccer',
                'description': 'Premium soccer trading cards featuring Premier League stars',
                'total_cards': 300
            },
            {
                'name': 'Champions League Chrome',
                'brand': 'TOPPS',
                'release_year': 2024,
                'sport': 'Soccer',
                'description': 'Chrome finish cards featuring UEFA Champions League players',
                'total_cards': 250
            },
            {
                'name': 'World Cup Stickers',
                'brand': 'PANINI',
                'release_year': 2022,
                'sport': 'Soccer',
                'description': 'Official FIFA World Cup Qatar 2022 sticker collection',
                'total_cards': 670
            },
            {
                'name': 'Select Soccer',
                'brand': 'PANINI',
                'release_year': 2024,
                'sport': 'Soccer',
                'description': 'High-end soccer cards with premium design',
                'total_cards': 200
            },
            {
                'name': 'Finest Soccer',
                'brand': 'TOPPS',
                'release_year': 2023,
                'sport': 'Soccer',
                'description': 'Ultra-premium cards with refractor technology',
                'total_cards': 150
            }
        ]

        for set_data in card_sets:
            card_set = CardSet.objects.create(**set_data)
            self.stdout.write(f'Created card set: {card_set}')

        # Get created objects for Cards
        all_players = list(Player.objects.all())
        all_sets = list(CardSet.objects.all())

        # Create Cards
        cards_data = [
            {
                'player': Player.objects.get(last_name='Messi'),
                'set': CardSet.objects.get(name='Prizm Premier League'),
                'card_number': '1',
                'rarity': 'LEGENDARY',
                'serial_number': '001/25',
                'image': 'https://i.ebayimg.com/images/g/2pYAAOSwB5Vkbz5X/s-l1600.jpg',
                'estimated_value': Decimal('2500.00')
            },
            {
                'player': Player.objects.get(last_name='Ronaldo'),
                'set': CardSet.objects.get(name='Champions League Chrome'),
                'card_number': '7',
                'rarity': 'ULTRA_RARE',
                'serial_number': '007/50',
                'image': 'https://i.ebayimg.com/images/g/JYwAAOSwfW5kW3Yz/s-l1600.jpg',
                'estimated_value': Decimal('1800.00')
            },
            {
                'player': Player.objects.get(last_name='Mbappe'),
                'set': CardSet.objects.get(name='World Cup Stickers'),
                'card_number': '10',
                'rarity': 'ROOKIE',
                'image': 'https://i.ebayimg.com/images/g/FE8AAOSwvTdkR1bH/s-l1600.jpg',
                'estimated_value': Decimal('450.00')
            },
            {
                'player': Player.objects.get(last_name='Haaland'),
                'set': CardSet.objects.get(name='Select Soccer'),
                'card_number': '9',
                'rarity': 'RARE',
                'serial_number': '123/199',
                'image': 'https://i.ebayimg.com/images/g/9r4AAOSwvK5kPqWt/s-l1600.jpg',
                'estimated_value': Decimal('750.00')
            },
            {
                'player': Player.objects.get(last_name='De Bruyne'),
                'set': CardSet.objects.get(name='Finest Soccer'),
                'card_number': '17',
                'rarity': 'AUTOGRAPH',
                'image': 'https://i.ebayimg.com/images/g/B8cAAOSwDLtkEm5q/s-l1600.jpg',
                'estimated_value': Decimal('1200.00')
            }
        ]

        for card_data in cards_data:
            card = Card.objects.create(**card_data)
            self.stdout.write(f'Created card: {card}')

        # Create a test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='collector1',
            defaults={
                'email': 'collector1@example.com',
                'first_name': 'John',
                'last_name': 'Collector'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(f'Created user: {user}')

        # Create UserCards (user collection)
        user_cards_data = [
            {
                'user': user,
                'card': Card.objects.get(player__last_name='Messi'),
                'purchase_price': Decimal('2000.00'),
                'purchase_date': date(2024, 1, 15),
                'grade': 'PSA',
                'grade_score': 9,
                'condition_note': 'Near perfect condition with slight corner wear',
                'for_sale': False
            },
            {
                'user': user,
                'card': Card.objects.get(player__last_name='Mbappe'),
                'purchase_price': Decimal('300.00'),
                'purchase_date': date(2024, 3, 10),
                'grade': 'UNGRADED',
                'condition_note': 'Mint condition, pack fresh',
                'for_sale': True,
                'sale_price': Decimal('500.00')
            },
            {
                'user': user,
                'card': Card.objects.get(player__last_name='Haaland'),
                'purchase_price': Decimal('600.00'),
                'purchase_date': date(2024, 2, 20),
                'grade': 'BGS',
                'grade_score': 8,
                'condition_note': 'Good condition with minor edge wear',
                'for_sale': False
            }
        ]

        for user_card_data in user_cards_data:
            user_card = UserCard.objects.create(**user_card_data)
            self.stdout.write(f'Created user card: {user_card}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded initial data:\n'
                f'- {Player.objects.count()} players\n'
                f'- {CardSet.objects.count()} card sets\n'
                f'- {Card.objects.count()} cards\n'
                f'- {UserCard.objects.count()} user cards'
            )
        )
