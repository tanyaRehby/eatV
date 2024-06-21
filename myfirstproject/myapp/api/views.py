from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import LoginSerializer, SignupSerializer, placeSerializer, LocationSerializer, ReverseGeocodeSerializer, UserSerializer
from myapp.models import Place, User, CustomUserManager
import requests
from rest_framework.views import APIView
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


##api.route('api/login/' , methods =['GET'])

@api_view(['GET', 'POST'])
def getRoutes(request):
    if request.method == 'GET':
        data = {
            'message': 'This is a GET request',
            'routes': [
                'GET /api',
                'GET /api/places',
                'POST /api/places/create',
                'POST /api/geocode/',
                'POST /api/reverse-geocode/',
                'POST /api/signup/',
                'GET /api/login',
            ]
        }
        return Response(data)
    
    if request.method == 'POST':
        posted_data = request.data
        return Response({'message': 'Data received', 'data': posted_data}, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    serializer_class = LoginSerializer

    def get(self, request, *args, **kwargs):
        print("backend LoginView")
        serializer = self.serializer_class(data=request.query_params)
        print("step0")
        if serializer.is_valid():
            print("step1")
            user = serializer.validated_data
            return Response({
                "user": UserSerializer(user).data,
                "message": "Login successful"
            }, status=status.HTTP_200_OK)
        print("step3")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        print("SignupView 0")
        serializer = self.serializer_class(data=request.data)
        print("data is ", request.data)

        if serializer.is_valid():
            print("SignupView 2")
            user = serializer.save()
            return Response({
                "user": UserSerializer(user).data,
                "message": "Signup successful"
            }, status=status.HTTP_201_CREATED)
        print("SignupView 3")
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
            api_key = 'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'  # Replace with your actual API key
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'}"
            response = requests.get(url)
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReverseGeocodeView(APIView):
    def get(self, request):
        print("backend 11")
        serializer = ReverseGeocodeSerializer(data=request.data)
        if serializer.is_valid():
            lat = serializer.validated_data['lat']
            lng = serializer.validated_data['lng']
            api_key = 'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'  # Replace with your actual API key
            url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'}"
            response = requests.get(url)
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def getPlaces(request):
    places = Place.objects.all()
    print(places)
    serializer = placeSerializer(places, many=True)
    print(serializer.data)
    return Response(serializer.data)

@api_view(['POST'])
def createPlace(request):
    serializer = placeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
