from .models import *
from rest_framework import serializers


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TouristDestinationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristDestination
        fields = ['id', 'place_name', 'weather', 'state', 'district', 'category', 'google_map_link', 'description', 'main_image', 'landmark']