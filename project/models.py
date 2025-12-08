from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from decimal import Decimal

# Profile model for user avatars, friends, and favorites
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True, related_name='friends_with')
    favorite_cards = models.ManyToManyField('Card', blank=True, related_name='favored_by')
    wishlist = models.ManyToManyField('Card', blank=True, related_name='wishlisted_by')
    trade_list = models.ManyToManyField('Card', blank=True, related_name='trade_listed_by')

    def __str__(self):
        return f"Profile: {self.user.username}"

    @property
    def num_friends(self):
        return self.friends.count()

    @property
    def num_favorites(self):
        return self.favorite_cards.count()

    @property
    def collection_value(self):
        return sum([uc.current_value_estimate for uc in self.user.user_cards.all()])

# Signal to auto-create Profile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Player(models.Model):
    """
    Standalone model representing soccer players.
    Each player exists independently and can be referenced by multiple cards.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=[
        ('GK', 'Goalkeeper'),
        ('CB', 'Center Back'),
        ('LB', 'Left Back'),
        ('RB', 'Right Back'),
        ('CM', 'Central Midfielder'),
        ('LM', 'Left Midfielder'),
        ('RM', 'Right Midfielder'),
        ('CAM', 'Central Attacking Midfielder'),
        ('LW', 'Left Winger'),
        ('RW', 'Right Winger'),
        ('ST', 'Striker'),
        ('CF', 'Center Forward'),
    ])
    club_team = models.CharField(max_length=100)
    birth_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1950), MaxValueValidator(2010)]
    )
    image = models.URLField(blank=True, null=True, help_text="URL to player image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.club_team}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from datetime import datetime
        return datetime.now().year - self.birth_year


class CardSet(models.Model):
    """
    Standalone model representing trading card product lines/sets.
    Each set exists independently and can contain multiple cards.
    """
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, choices=[
        ('PANINI', 'Panini'),
        ('TOPPS', 'Topps'),
        ('UPPER_DECK', 'Upper Deck'),
        ('LEAF', 'Leaf Trading Cards'),
        ('FUTERA', 'Futera'),
        ('OTHER', 'Other'),
    ])
    release_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1990), MaxValueValidator(2025)]
    )
    sport = models.CharField(max_length=50, default='Soccer')
    description = models.TextField(blank=True, null=True)
    total_cards = models.PositiveIntegerField(null=True, blank=True, help_text="Total number of cards in set")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-release_year', 'name']
        
    def __str__(self):
        return f"{self.release_year} {self.brand} {self.name}"


class Card(models.Model):
    """
    Model representing individual trading cards.
    Each card belongs to one player and one card set.
    """
    RARITY_CHOICES = [
        ('COMMON', 'Common'),
        ('UNCOMMON', 'Uncommon'),
        ('RARE', 'Rare'),
        ('ULTRA_RARE', 'Ultra Rare'),
        ('LEGENDARY', 'Legendary'),
        ('ROOKIE', 'Rookie Card'),
        ('AUTOGRAPH', 'Autograph'),
        ('PATCH', 'Patch Card'),
        ('SERIAL', 'Serial Numbered'),
        ('PRIZM', 'Prizm'),
    ]

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='cards')
    set = models.ForeignKey(CardSet, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=20, help_text="Card number within the set")
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES)
    serial_number = models.CharField(max_length=50, blank=True, null=True, help_text="Serial number if numbered card")
    image = models.URLField(blank=True, null=True, help_text="URL to card image")
    estimated_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Estimated market value in USD"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['set__release_year', 'set__name', 'card_number']
        unique_together = ['set', 'card_number']  # Prevent duplicate card numbers in same set
        
    def __str__(self):
        return f"{self.set} - #{self.card_number} {self.player.full_name}"

    @property
    def is_numbered(self):
        return bool(self.serial_number)


class UserCard(models.Model):
    """
    Model representing cards owned by users.
    Supports CRUD operations for user collections.
    """
    CONDITION_CHOICES = [
        ('MINT', 'Mint (10)'),
        ('NEAR_MINT', 'Near Mint (9)'),
        ('EXCELLENT', 'Excellent (8)'),
        ('VERY_GOOD', 'Very Good (7)'),
        ('GOOD', 'Good (6)'),
        ('FAIR', 'Fair (5)'),
        ('POOR', 'Poor (1-4)'),
    ]

    GRADE_CHOICES = [
        ('UNGRADED', 'Ungraded'),
        ('PSA', 'PSA'),
        ('BGS', 'Beckett'),
        ('SGC', 'SGC'),
        ('CGC', 'CGC'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cards')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='owned_by')
    purchase_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Price paid for this card"
    )
    purchase_date = models.DateField()
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, default='UNGRADED')
    grade_score = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Numerical grade if professionally graded"
    )
    condition_note = models.TextField(blank=True, null=True, help_text="Additional condition notes")
    for_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Asking price if for sale"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.card}"

    @property
    def current_value_estimate(self):
        """Return the estimated current value based on condition and grading"""
        base_value = self.card.estimated_value
        
        # Adjust based on condition
        condition_multipliers = {
            'MINT': 1.0,
            'NEAR_MINT': 0.85,
            'EXCELLENT': 0.70,
            'VERY_GOOD': 0.55,
            'GOOD': 0.40,
            'FAIR': 0.25,
            'POOR': 0.10,
        }
        
        multiplier = condition_multipliers.get(self.condition_note, 1.0)
        
        # Additional premium for professional grading
        if self.grade != 'UNGRADED' and self.grade_score:
            if self.grade_score >= 9:
                multiplier *= 1.5  # Premium for high grades
            elif self.grade_score >= 7:
                multiplier *= 1.2  # Moderate premium
                
        return base_value * Decimal(str(multiplier))

    @property 
    def profit_loss(self):
        """Calculate profit/loss if sold at current estimate"""
        return self.current_value_estimate - self.purchase_price
