from rest_framework.serializers import ModelSerializer
from myapp.models import Place, User, CustomUserManager
import json
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'is_business_owner']

    def create(self, validated_data):
        print(validated_data['email'])
        user = User.objects.create(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            is_business_owner=validated_data.get('is_business_owner', False),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['place_name', 'city', 'address', 'longitude', 'latitude', 'food_category', 'is_kosher', 'has_vegan_option', 'recommended_dishes', 'image', 'link']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        print("val1")
        user = authenticate(email=data['email'], password=data['password'])
        print(user)
        if user and user.is_active:
            print("error")
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

    # maps/serializers.py

class ReverseGeocodeSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()