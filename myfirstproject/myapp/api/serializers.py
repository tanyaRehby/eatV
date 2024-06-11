from rest_framework.serializers import ModelSerializer
from myapp.models import Place
import json
from rest_framework import serializers


class placeSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class LocationSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)
    # maps/serializers.py
class ReverseGeocodeSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()
