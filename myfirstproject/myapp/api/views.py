from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import LoginSerializer, SignupSerializer, PlaceSerializer, LocationSerializer, ReverseGeocodeSerializer, UserSerializer
from myapp.models import Place, User, CustomUserManager
import requests
from rest_framework.views import APIView
from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .services import plan_tour

User = get_user_model()

@api_view(['POST'])
def register(request):
    user_serializer = SignupSerializer(data=request.data)
    place_serializer = None
    if 'is_business_owner' in request.data and request.data['is_business_owner'] == 'True':
        place_serializer = PlaceSerializer(data=request.data)
    if user_serializer.is_valid() and (place_serializer is None or place_serializer.is_valid()):
        user = user_serializer.save()
        if place_serializer:
            place = place_serializer.save(user=user)
        return Response({"detail": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
                "user": UserSerializer(user).data,
                "message": "Login successful"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SignupView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user).data,
                "message": "Signup successful"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            api_key = 'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'  
            url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
            response = requests.get(url)
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReverseGeocodeView(APIView):
    def post(self, request):
        serializer = ReverseGeocodeSerializer(data=request.data)
        if serializer.is_valid():
            lat = serializer.validated_data['lat']
            lng = serializer.validated_data['lng']
            api_key = 'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'  
            url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={api_key}"
            response = requests.get(url)
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getPlaces(request):
    places = Place.objects.all()
    serializer = PlaceSerializer(places, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createPlace(request):
    serializer = PlaceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class tourView(APIView):
    def post(self, request):
        address = request.data.get('address')
        kosher = request.data.get('kosher', False)
        vegan = request.data.get('vegan', False)
        num_stops = request.data.get('num_stops', 5)
        try:
            num_stops = int(num_stops)
        except ValueError:
            return Response({"error": "num_stops must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        tour = plan_tour(address, kosher, vegan, num_stops)
        
        if tour is not None:
            serialized_tour = [{
                'place_name': place.place_name,
                'city': place.city,
                'address': place.address,
                'food_category': place.food_category,
                'latitude': place.latitude,
                'longitude': place.longitude,
            } for place in tour]
            return Response(serialized_tour, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No suitable route found'}, status=status.HTTP_400_BAD_REQUEST)