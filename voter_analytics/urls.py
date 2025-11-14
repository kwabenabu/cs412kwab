"""
File: voter_analytics/urls.py
Author: Kwabena <kwabena@bu.edu>
Description: URL configuration for voter analytics application. Maps URLs to views
for voter list, detail, and analytics pages.

Reference: Django URL dispatcher - https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.urls import path
from .views import VoterListView, VoterDetailView, GraphsView

app_name = 'voter_analytics'

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),
    path('graphs/', GraphsView.as_view(), name='graphs'),
]
