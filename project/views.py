
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count, Avg, Sum, Max
from django.urls import reverse_lazy
from .models import Player, CardSet, Card, UserCard
from .forms import AddCardToCollectionForm, EditUserCardForm, CardSearchForm, UserRegisterForm, ProfileEditForm

# User registration, login, logout, and profile edit views
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project:home')
    else:
        form = UserRegisterForm()
    return render(request, 'project/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('project:home')
    else:
        form = AuthenticationForm()
    return render(request, 'project/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('project:home')

@login_required
def profile_edit_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('project:profile_edit')
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, 'project/profile_edit.html', {'form': form})

# REST Framework imports
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PlayerSerializer, CardSerializer

# API Views
class PlayerListAPI(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class CardListAPI(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class HomeView(TemplateView):
    """
    Home page showing overview statistics and recent additions.
    """
    template_name = 'project/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistics
        context['total_players'] = Player.objects.count()
        context['total_cards'] = Card.objects.count()
        context['total_sets'] = CardSet.objects.count()
        
        # Recent additions
        context['recent_players'] = Player.objects.order_by('-created_at')[:3]
        context['recent_cards'] = Card.objects.order_by('-created_at')[:5]
        
        # Valuable cards
        context['valuable_cards'] = Card.objects.order_by('-estimated_value')[:5]
        
        # User collection stats (if user is authenticated)
        if self.request.user.is_authenticated:
            user_collection = UserCard.objects.filter(user=self.request.user)
            context['collection_count'] = user_collection.count()
            context['collection_value'] = user_collection.aggregate(
                total=Sum('purchase_price')
            )['total'] or 0
        
        return context


class PlayerListView(ListView):
    """
    Display all players with filtering and sorting options.
    """
    model = Player
    template_name = 'project/player_list.html'
    context_object_name = 'players'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Player.objects.annotate(card_count=Count('cards'))
        
        # Filter by position
        position = self.request.GET.get('position')
        if position:
            queryset = queryset.filter(position=position)
        
        # Filter by country
        country = self.request.GET.get('country')
        if country:
            queryset = queryset.filter(country__icontains=country)
        
        # Filter by team
        team = self.request.GET.get('team')
        if team:
            queryset = queryset.filter(club_team__icontains=team)
        
        # Sort by
        sort_by = self.request.GET.get('sort', 'last_name')
        if sort_by in ['last_name', '-card_count', 'birth_year', '-birth_year']:
            queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['positions'] = Player._meta.get_field('position').choices
        context['current_position'] = self.request.GET.get('position', '')
        context['current_country'] = self.request.GET.get('country', '')
        context['current_team'] = self.request.GET.get('team', '')
        context['current_sort'] = self.request.GET.get('sort', 'last_name')
        return context


class PlayerDetailView(DetailView):
    """
    Display detailed information about a specific player.
    """
    model = Player
    template_name = 'project/player_detail.html'
    context_object_name = 'player'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = self.get_object()
        
        # Get all cards for this player
        context['cards'] = Card.objects.filter(player=player).select_related('set')
        
        # Calculate statistics
        player_cards = Card.objects.filter(player=player)
        context['total_cards'] = player_cards.count()
        context['avg_value'] = player_cards.aggregate(avg=Avg('estimated_value'))['avg']
        context['max_value'] = player_cards.aggregate(max=Max('estimated_value'))['max']
        
        return context


class CardSetListView(ListView):
    """
    Display all card sets with filtering options.
    """
    model = CardSet
    template_name = 'project/cardset_list.html'
    context_object_name = 'card_sets'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = CardSet.objects.annotate(card_count=Count('cards'))
        
        # Filter by brand
        brand = self.request.GET.get('brand')
        if brand:
            queryset = queryset.filter(brand=brand)
        
        # Filter by year range
        year_from = self.request.GET.get('year_from')
        year_to = self.request.GET.get('year_to')
        if year_from:
            queryset = queryset.filter(release_year__gte=year_from)
        if year_to:
            queryset = queryset.filter(release_year__lte=year_to)
        
        # Sort
        sort_by = self.request.GET.get('sort', '-release_year')
        if sort_by in ['-release_year', 'release_year', 'name', '-card_count']:
            queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = CardSet.objects.values_list('brand', flat=True).distinct()
        context['current_brand'] = self.request.GET.get('brand', '')
        context['current_year_from'] = self.request.GET.get('year_from', '')
        context['current_year_to'] = self.request.GET.get('year_to', '')
        context['current_sort'] = self.request.GET.get('sort', '-release_year')
        return context


class CardSetDetailView(DetailView):
    """
    Display detailed information about a specific card set.
    """
    model = CardSet
    template_name = 'project/cardset_detail.html'
    context_object_name = 'card_set'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card_set = self.get_object()
        
        # Get all cards in this set
        context['cards'] = Card.objects.filter(set=card_set).select_related('player')
        
        # Statistics
        set_cards = Card.objects.filter(set=card_set)
        context['total_cards'] = set_cards.count()
        context['avg_value'] = set_cards.aggregate(avg=Avg('estimated_value'))['avg']
        context['total_value'] = set_cards.aggregate(total=Sum('estimated_value'))['total']
        
        return context


class CardListView(ListView):
    """
    Display all cards with advanced filtering options.
    """
    model = Card
    template_name = 'project/card_list.html'
    context_object_name = 'cards'
    paginate_by = 24
    
    def get_queryset(self):
        queryset = Card.objects.select_related('player', 'set')
        
        # Filter by rarity
        rarity = self.request.GET.get('rarity')
        if rarity:
            queryset = queryset.filter(rarity=rarity)
        
        # Filter by player name
        player_name = self.request.GET.get('player')
        if player_name:
            queryset = queryset.filter(
                Q(player__first_name__icontains=player_name) |
                Q(player__last_name__icontains=player_name)
            )
        
        # Filter by set
        card_set = self.request.GET.get('set')
        if card_set:
            queryset = queryset.filter(set__id=card_set)
        
        # Filter by value range
        min_value = self.request.GET.get('min_value')
        max_value = self.request.GET.get('max_value')
        if min_value:
            queryset = queryset.filter(estimated_value__gte=min_value)
        if max_value:
            queryset = queryset.filter(estimated_value__lte=max_value)
        
        # Sort
        sort_by = self.request.GET.get('sort', '-estimated_value')
        if sort_by in ['-estimated_value', 'estimated_value', 'player__last_name', '-created_at']:
            queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rarities'] = Card.RARITY_CHOICES
        context['card_sets'] = CardSet.objects.all()
        context['current_rarity'] = self.request.GET.get('rarity', '')
        context['current_player'] = self.request.GET.get('player', '')
        context['current_set'] = self.request.GET.get('set', '')
        context['current_min_value'] = self.request.GET.get('min_value', '')
        context['current_max_value'] = self.request.GET.get('max_value', '')
        context['current_sort'] = self.request.GET.get('sort', '-estimated_value')
        return context


class CardDetailView(DetailView):
    """
    Display detailed information about a specific card.
    """
    model = Card
    template_name = 'project/card_detail.html'
    context_object_name = 'card'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card = self.get_object()
        
        # Check if current user owns this card
        if self.request.user.is_authenticated:
            context['user_owns'] = UserCard.objects.filter(
                user=self.request.user, 
                card=card
            ).exists()
            context['user_card'] = UserCard.objects.filter(
                user=self.request.user, 
                card=card
            ).first()
        
        # Similar cards (same player or same set)
        context['similar_cards'] = Card.objects.filter(
            Q(player=card.player) | Q(set=card.set)
        ).exclude(id=card.id)[:6]
        
        return context


class UserCardListView(LoginRequiredMixin, ListView):
    """
    Display current user's card collection.
    """
    model = UserCard
    template_name = 'project/user_collection.html'
    context_object_name = 'user_cards'
    paginate_by = 20
    
    def get_queryset(self):
        return UserCard.objects.filter(user=self.request.user).select_related('card__player', 'card__set')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_cards = UserCard.objects.filter(user=self.request.user)
        
        # Collection statistics
        context['collection_stats'] = {
            'total_cards': user_cards.count(),
            'total_invested': user_cards.aggregate(total=Sum('purchase_price'))['total'] or 0,
            'estimated_value': sum([uc.current_value_estimate for uc in user_cards]),
            'cards_for_sale': user_cards.filter(for_sale=True).count(),
        }
        
        return context


class UserCardDetailView(LoginRequiredMixin, DetailView):
    """
    Display detailed information about a user's card.
    """
    model = UserCard
    template_name = 'project/usercard_detail.html'
    context_object_name = 'user_card'
    
    def get_queryset(self):
        return UserCard.objects.filter(user=self.request.user)


class AddCardToCollectionView(LoginRequiredMixin, CreateView):
    """
    Form to add a card to user's collection.
    """
    model = UserCard
    form_class = AddCardToCollectionForm
    template_name = 'project/add_card_form.html'
    success_url = reverse_lazy('project:user_collection')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Card added to your collection!')
        return super().form_valid(form)


class EditUserCardView(LoginRequiredMixin, UpdateView):
    """
    Form to edit a card in user's collection.
    """
    model = UserCard
    form_class = EditUserCardForm
    template_name = 'project/edit_usercard_form.html'
    
    def get_queryset(self):
        return UserCard.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('project:usercard_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Card information updated!')
        return super().form_valid(form)


class CardSearchView(TemplateView):
    """
    Advanced search functionality for cards.
    """
    template_name = 'project/card_search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CardSearchForm(self.request.GET or None)
        
        if self.request.GET:
            form = CardSearchForm(self.request.GET)
            if form.is_valid():
                # Perform search based on form data
                queryset = Card.objects.select_related('player', 'set')
                
                # Apply filters from form
                if form.cleaned_data['player_name']:
                    queryset = queryset.filter(
                        Q(player__first_name__icontains=form.cleaned_data['player_name']) |
                        Q(player__last_name__icontains=form.cleaned_data['player_name'])
                    )
                
                if form.cleaned_data['rarity']:
                    queryset = queryset.filter(rarity=form.cleaned_data['rarity'])
                
                if form.cleaned_data['min_value']:
                    queryset = queryset.filter(estimated_value__gte=form.cleaned_data['min_value'])
                
                if form.cleaned_data['max_value']:
                    queryset = queryset.filter(estimated_value__lte=form.cleaned_data['max_value'])
                
                context['search_results'] = queryset[:50]  # Limit results
        
        return context


class CardSetCreateView(CreateView):
    model = CardSet
    fields = ['name', 'release_year', 'brand', 'sport']
    template_name = 'project/cardset_form.html'
    success_url = reverse_lazy('project:cardset_list')


class CardCreateView(CreateView):
    model = Card
    fields = ['player', 'set', 'card_number', 'rarity', 'serial_number', 'image', 'estimated_value']
    template_name = 'project/card_form.html'
    success_url = reverse_lazy('project:card_list')


class UserCardCreateView(CreateView):
    model = UserCard
    fields = ['card', 'purchase_price', 'purchase_date', 'grade', 'grade_score', 'condition_note', 'for_sale', 'sale_price']
    template_name = 'project/usercard_form.html'
    success_url = reverse_lazy('project:user_collection')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PlayerCreateView(CreateView):
    model = Player
    fields = ['first_name', 'last_name', 'full_name', 'birth_year', 'country', 'club_team', 'position', 'image']
    template_name = 'project/player_form.html'
    success_url = reverse_lazy('project:player_list')


class PlayerUpdateView(UpdateView):
    model = Player
    fields = ['first_name', 'last_name', 'full_name', 'birth_year', 'country', 'club_team', 'position', 'image']
    template_name = 'project/player_form.html'
    success_url = reverse_lazy('project:player_list')


class PlayerDeleteView(DeleteView):
    model = Player
    template_name = 'project/player_confirm_delete.html'
    success_url = reverse_lazy('project:player_list')


class CardUpdateView(UpdateView):
    model = Card
    fields = ['player', 'set', 'card_number', 'rarity', 'serial_number', 'image', 'estimated_value']
    template_name = 'project/card_form.html'
    success_url = reverse_lazy('project:card_list')


class CardDeleteView(DeleteView):
    model = Card
    template_name = 'project/card_confirm_delete.html'
    success_url = reverse_lazy('project:card_list')


class UserCardUpdateView(UpdateView):
    model = UserCard
    fields = ['card', 'purchase_price', 'purchase_date', 'grade', 'grade_score', 'condition_note', 'for_sale', 'sale_price']
    template_name = 'project/usercard_form.html'
    success_url = reverse_lazy('project:user_collection')


class UserCardDeleteView(DeleteView):
    model = UserCard
    template_name = 'project/usercard_confirm_delete.html'
    success_url = reverse_lazy('project:user_collection')


class CardSetUpdateView(UpdateView):
    model = CardSet
    fields = ['name', 'release_year', 'brand', 'sport']
    template_name = 'project/cardset_form.html'
    success_url = reverse_lazy('project:cardset_list')


class CardSetDeleteView(DeleteView):
    model = CardSet
    template_name = 'project/cardset_confirm_delete.html'
    success_url = reverse_lazy('project:cardset_list')
