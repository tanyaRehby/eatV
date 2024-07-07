from rest_framework.serializers import ModelSerializer
from myapp.models import Place, User, CustomUserManager
import json
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
import requests

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    print("1")
    password = serializers.CharField(write_only=True)
    class Meta:
        print("3")
        model = User
        fields = ['email', 'full_name', 'password', 'is_business_owner']
    def create(self, validated_data):
        print("2")
        user = User.objects.create(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            is_business_owner=validated_data.get('is_business_owner', False),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class PlaceSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    link = serializers.URLField(required=False, allow_blank=True)
   
    class Meta:
        model = Place
        fields = ['place_name', 'city', 'address', 'food_category', 'is_kosher', 'has_vegan_option', 'recommended_dishes', 'image', 'link', 'latitude', 'longitude']
    
    def create(self, validated_data):
        address = validated_data['address']
        city=validated_data['city']
        full_address = f"{address}, {city}"
        api_key = 'AIzaSyAJLe6L_bHnzqC6K3YO0ET_iw7D1gmo07I'
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={full_address}&key={api_key}'
        response = requests.get(url)
        response_data = response.json()
        if response_data['status'] == 'OK':
            location = response_data['results'][0]['geometry']['location']
            latitude = float(location['lat'])
            longitude = float(location['lng'])
        else:
            latitude = None
            longitude = None
     
        place = Place.objects.create(
            latitude=latitude,
            longitude=longitude,
            place_name=validated_data['place_name'],
            address = validated_data['address'],
            city = validated_data['city'],
            food_category=validated_data['food_category'],
            is_kosher=validated_data['is_kosher'],
            has_vegan_option=validated_data['has_vegan_option'],
            recommended_dishes=validated_data['recommended_dishes'],
            image=validated_data.get('image', None),
            link=validated_data.get('link', False),
            )
     
        return Place
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'is_business_owner', 'is_staff', 'is_superuser', 'is_active']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class placeSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class LocationSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)

class ReverseGeocodeSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()