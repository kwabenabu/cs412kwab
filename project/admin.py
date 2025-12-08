from django.contrib import admin
from .models import Player, CardSet, Card, UserCard, Profile

# Inline for UserCard in User admin (optional, if you want to show user cards in User admin)
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserCardInline(admin.TabularInline):
    model = UserCard
    extra = 0

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, UserCardInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'num_friends', 'num_favorites', 'collection_value']
    search_fields = ['user__username', 'bio']
    filter_horizontal = ['friends', 'favorite_cards', 'wishlist', 'trade_list']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'club_team', 'country', 'birth_year', 'age']
    list_filter = ['position', 'club_team', 'country', 'birth_year']
    search_fields = ['first_name', 'last_name', 'club_team', 'country']
    ordering = ['last_name', 'first_name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'birth_year')
        }),
        ('Career Details', {
            'fields': ('position', 'club_team', 'country')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )


@admin.register(CardSet)
class CardSetAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'release_year', 'sport', 'total_cards']
    list_filter = ['brand', 'release_year', 'sport']
    search_fields = ['name', 'brand', 'description']
    ordering = ['-release_year', 'name']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'rarity', 'estimated_value', 'is_numbered', 'created_at']
    list_filter = ['rarity', 'set__brand', 'set__release_year', 'serial_number']
    search_fields = ['player__first_name', 'player__last_name', 'set__name', 'card_number']
    ordering = ['set__release_year', 'set__name', 'card_number']
    
    fieldsets = (
        ('Card Details', {
            'fields': ('player', 'set', 'card_number', 'rarity')
        }),
        ('Special Features', {
            'fields': ('serial_number', 'image')
        }),
        ('Valuation', {
            'fields': ('estimated_value',)
        }),
    )


@admin.register(UserCard)
class UserCardAdmin(admin.ModelAdmin):
    list_display = ['user', 'card', 'purchase_price', 'current_value_estimate', 'profit_loss', 'grade', 'for_sale']
    list_filter = ['grade', 'for_sale', 'purchase_date', 'card__rarity']
    search_fields = ['user__username', 'card__player__first_name', 'card__player__last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Ownership', {
            'fields': ('user', 'card')
        }),
        ('Purchase Information', {
            'fields': ('purchase_price', 'purchase_date')
        }),
        ('Condition & Grading', {
            'fields': ('grade', 'grade_score', 'condition_note')
        }),
        ('Marketplace', {
            'fields': ('for_sale', 'sale_price')
        }),
    )
    
    readonly_fields = ['current_value_estimate', 'profit_loss']
