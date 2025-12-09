from django.urls import path
from django.views.generic import TemplateView

from . import views
from django.contrib.auth import views as auth_views

app_name = 'project'

urlpatterns = [

    # User auth/profile
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logged_out/', TemplateView.as_view(template_name='project/logged_out.html'), name='logout_confirmation'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),

    # Home page
    path('', views.HomeView.as_view(), name='home'),

    # API endpoints for React Native app
    path('api/players/', views.PlayerListAPI.as_view(), name='api_player_list'),
    path('api/cards/', views.CardListAPI.as_view(), name='api_card_list'),
    
    # Player views
    path('players/', views.PlayerListView.as_view(), name='player_list'),
    path('player/<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
    path('player/create/', views.PlayerCreateView.as_view(), name='player_create'),
    path('player/<int:pk>/edit/', views.PlayerUpdateView.as_view(), name='player_update'),
    path('player/<int:pk>/delete/', views.PlayerDeleteView.as_view(), name='player_delete'),
    
    # Card Set views
    path('sets/', views.CardSetListView.as_view(), name='cardset_list'),
    path('set/<int:pk>/', views.CardSetDetailView.as_view(), name='cardset_detail'),
    path('set/<int:pk>/edit/', views.CardSetUpdateView.as_view(), name='cardset_update'),
    path('set/<int:pk>/delete/', views.CardSetDeleteView.as_view(), name='cardset_delete'),
    
    # Card views
    path('cards/', views.CardListView.as_view(), name='card_list'),
    path('card/<int:pk>/', views.CardDetailView.as_view(), name='card_detail'),
        path('card/<int:pk>/edit/', views.CardUpdateView.as_view(), name='card_update'),
        path('card/<int:pk>/delete/', views.CardDeleteView.as_view(), name='card_delete'),
    
    # User Collection views
    path('collection/', views.UserCardListView.as_view(), name='user_collection'),
    path('collection/<int:pk>/', views.UserCardDetailView.as_view(), name='usercard_detail'),
        path('collection/<int:pk>/edit/', views.UserCardUpdateView.as_view(), name='usercard_update'),
        path('collection/<int:pk>/delete/', views.UserCardDeleteView.as_view(), name='usercard_delete'),
    
    # Form views for interactions
    path('add-card/', views.AddCardToCollectionView.as_view(), name='add_card'),
    path('collection/<int:pk>/edit/', views.EditUserCardView.as_view(), name='edit_usercard'),
    path('search/', views.CardSearchView.as_view(), name='card_search'),
    # Create views for CardSet, Card, and UserCard
    path('set/create/', views.CardSetCreateView.as_view(), name='cardset_create'),
    path('card/create/', views.CardCreateView.as_view(), name='card_create'),
    path('collection/create/', views.UserCardCreateView.as_view(), name='usercard_create'),
]
