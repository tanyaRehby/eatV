from rest_framework.serializers import ModelSerializer
from myapp.models import Place
import json
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

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
        fields = ('email', 'full_name', 'is_business_owner', 'business_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'is_business_owner', 'business_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            is_business_owner=validated_data.get('is_business_owner', False),
            business_name=validated_data.get('business_name', '')
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