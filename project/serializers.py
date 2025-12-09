"""
File: project/serializers.py
Author: kwabena kwabena@bu.edu
Description: DRF serializers for Player and Card models in the trading card app.
"""
from rest_framework import serializers
from .models import Player, Card

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
