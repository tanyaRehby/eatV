from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import placeSerializer, LocationSerializer, ReverseGeocodeSerializer
from myapp.models import Place, User, CustomUserManager
import requests
from rest_framework.views import APIView

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": "success", "user": user.email})
        else:
            return JsonResponse({"status": "fail", "message": "Invalid credentials"}, status=400)

@csrf_exempt
def password_reset_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        # Add your password reset logic here
        return JsonResponse({"status": "success", "message": "Email has been sent to you"})

class GeocodeView(APIView):
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            address = serializer.validated_data['address']
            api_key = 'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'  # Replace with your actual API key
            url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'}'
            response = requests.get(url)
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReverseGeocodeView(APIView):
    def post(self, request):
        serializer = ReverseGeocodeSerializer(data=request.data)
        if serializer.is_valid():
            lat = serializer.validated_data['lat']
            lng = serializer.validated_data['lng']
            api_key = 'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'  # Replace with your actual API key
            url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'}'
            response = requests.get(url)
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/places',
        'POST /api/places/create',
        'POST /api/geocode/',
        'POST /api/reverse-geocode/',
    ]
    return Response(routes)

@api_view(['GET'])
def getPlaces(request):
    places = Place.objects.all()
    serializer = placeSerializer(places, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createPlace(request):
    serializer = placeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
