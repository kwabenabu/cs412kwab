##mini_insta/urls.py
# file urls.py
# author Kwabena Ampomah
# description Urls for the mini_insta app
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Public read-only pages
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('profiles/', views.ProfileListView.as_view(), name='profile-list'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='show_post'),

    # Followers / Following (public)
    path('profile/<int:pk>/followers/', views.ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following/', views.ShowFollowingDetailView.as_view(), name='show_following'),

    # Auth-required owner actions (pk removed)
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/create_post/', views.CreatePostView.as_view(), name='create_post'),
    path('profile/feed/', views.PostFeedListView.as_view(), name='show_feed'),
    path('profile/search/', views.SearchView.as_view(), name='search'),

    # Registration (public)
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),

    # Authentication: login/logout
    path('login/', auth_views.LoginView.as_view(template_name='insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logged_out/', TemplateView.as_view(template_name='insta/logged_out.html'), name='logout_confirmation'),

    # Update and Delete post pages (owner-only via view guards)
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update/', views.UpdatePostView.as_view(), name='update_post'),

    # Follows & Likes (use POST)
    path('profile/<int:pk>/follow/', views.FollowView.as_view(), name='follow'),
    path('profile/<int:pk>/delete_follow/', views.UnfollowView.as_view(), name='delete_follow'),
    path('post/<int:pk>/like/', views.LikeView.as_view(), name='like'),
    path('post/<int:pk>/delete_like/', views.UnlikeView.as_view(), name='delete_like'),
]
